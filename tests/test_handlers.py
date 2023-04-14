from datetime import date

from domain import events, commands
from service import messagebus, unit_of_work
from tests.test_services import FakeUnitOfWork


class FakeMessageBus(messagebus.AbstractMessageBus):
    def __init__(self, uow: FakeUnitOfWork):
        super().__init__()
        self.uow = uow
        self.EVENT_HANDLERS = messagebus.EVENT_HANDLERS
        self.COMMAND_HANDLERS = messagebus.COMMAND_HANDLERS


class TestChangeBatchQuantity:

    def test_something(self):
        uow = unit_of_work.SqlAlchemyUnitOfWork()
        messBus = messagebus.MessageBus(uow)

    def test_changes_available_quantity(self):
        uow = FakeUnitOfWork()
        messBus = FakeMessageBus(uow)
        messBus.handle(commands.CreateBatch("batch1", "ADORABLE-SETTEE",100, None))
        [batch] = uow.products.get(sku="ADORABLE-SETTEE").batches
        assert batch.available_quantity == 100
        messBus.handle(commands.ChangeBatchQuantity("batch1", 50))
        assert batch.available_quantity == 50

    def test_mail_sent(self):
        messBus = FakeMessageBus(FakeUnitOfWork())
        info = messBus.handle(events.OutOfStock("ADORABLESETTEE"))
        assert info == ['mail sent']

    def test_reallocates_if_necessary(self):
        uow = FakeUnitOfWork()
        messBus = FakeMessageBus(uow)
        event_history = [
            commands.CreateBatch("batch1", "INDIFFERENT-TABLE", 50, None),
            commands.CreateBatch("batch2", "INDIFFERENT-TABLE", 50, date.today()),
            commands.Allocate("order1", "INDIFFERENT-TABLE", 20),
            commands.Allocate("order2", "INDIFFERENT-TABLE", 20),
        ]
        for e in event_history:
            messBus.handle(e)
        [batch1, batch2] = uow.products.get(sku="INDIFFERENT-TABLE").batches
        assert batch1.available_quantity == 10
        assert batch2.available_quantity == 50

        messBus.handle(commands.ChangeBatchQuantity("batch1", 25))
        # order1 or order2 will be deallocated, so we'll have 25 - 20
        assert batch1.available_quantity == 5
        # and 20 will be reallocated to the next batch