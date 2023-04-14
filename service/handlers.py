import email

from domain import events, model, commands
from service import unit_of_work
from service.services import InvalidSku


def add_batch(command: commands.CreateBatch, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        product = uow.products.get(sku=command.sku)
        if product is None:
            product = model.Product(command.sku, batches=[])
            uow.products.add(product)
            product = uow.products.get(sku=command.sku)
        product.batches.append(model.Batch(command.ref, command.sku, command.qty, command.eta))
        uow.commit()


def allocate(command: commands.Allocate, uow: unit_of_work.AbstractUnitOfWork) -> str:
    line = model.OrderLine(command.order_id, command.sku, command.qty)
    with uow:
        product = uow.products.get(sku=line.sku)
        if product is None:
            raise InvalidSku(f'Invalid sku {line.sku}')
        batchref = product.allocate(line)
        uow.commit()
        return batchref


def change_batch_quantity(command: commands.ChangeBatchQuantity, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        product = uow.products.get_by_batchref(batchref=command.ref)
        product.change_batch_quantity(ref= command.ref, qty=command.qty)
        uow.commit()


def send_out_of_stock_notification(event: events.OutOfStock, uow: unit_of_work.AbstractUnitOfWork):
    # email.send_mail(
    #     'kysydragon7@gmail.com',
    #     f'Out of stock for {event.sku}',
    # )
    return "mail sent"
