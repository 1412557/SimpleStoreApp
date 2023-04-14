import abc
import logging
from typing import Dict, Type, List, Callable, Union
from tenacity import Retrying, RetryError, stop_after_attempt, wait_exponential

from domain import events, commands
from service import unit_of_work
from service.handlers import send_out_of_stock_notification, add_batch, allocate, change_batch_quantity

Message = Union[commands.Command, events.Event]

EVENT_HANDLERS = {
        events.OutOfStock: [send_out_of_stock_notification],
    }

COMMAND_HANDLERS = {
    commands.Allocate: allocate,
    commands.CreateBatch: add_batch,
    commands.ChangeBatchQuantity: change_batch_quantity
}


class AbstractMessageBus(abc.ABC):
    EVENT_HANDLERS: Dict[Type[events.Event], List[Callable]]
    COMMAND_HANDLERS: Dict[Type[commands.Command], Callable]
    uow: unit_of_work.AbstractUnitOfWork

    def __init__(self):
        self.queue = []

    def handle(self, message: Message):
        self.queue = [message]
        result = []
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, events.Event):
                result.append(self._handle_event(message))
            elif isinstance(message, commands.Command):
                result.append(self._handle_command(message))
            else:
                raise Exception(f'{message} was not an Event or Command')
        return result

    def _handle_event(self, event: events.Event):
        result = ''
        for handler in self.EVENT_HANDLERS[type(event)]:
            try:
                for attemp in Retrying(stop=stop_after_attempt(3), wait=wait_exponential()):
                    with attemp:
                        logging.debug(f'handling event {event} with handler {handler}')
                        result = handler(event, self.uow)
                        self.queue.extend(self.uow.collect_new_events())
            except RetryError as retry_failure:
                logging.error(f'failed to handle event, retry {retry_failure.last_attempt.attempt_number} times')
                continue
        return result

    def _handle_command(self, command: commands.Command):
        logging.debug(f'handling command {command}')
        result = ''
        try:
            handler = self.COMMAND_HANDLERS[type(command)]
            result = handler(command, self.uow)
            self.queue.extend(self.uow.collect_new_events())
        except Exception:
            logging.exception('Exception handling command %s', command)
            raise
        return result


class MessageBus(AbstractMessageBus):

    def __init__(self, uow: unit_of_work.SqlAlchemyUnitOfWork):
        super().__init__()
        self.uow = uow
        self.EVENT_HANDLERS = EVENT_HANDLERS
        self.COMMAND_HANDLERS = COMMAND_HANDLERS




