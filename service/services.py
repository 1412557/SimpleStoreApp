from datetime import date
from typing import Optional

from domain import model
from service import unit_of_work, messagebus


class InvalidSku(Exception):
    pass


# def add_batch(ref: str, sku: str, qty: int, eta: Optional[date], uow: unit_of_work.AbstractUnitOfWork):
#     with uow:
#         product = uow.products.get(sku=sku)
#         if product is None:
#             product = model.Product(sku, batches=[])
#             uow.products.add(product)
#         product.batches.append(model.Batch(ref, sku, qty, eta))
#         uow.commit()


# def allocate(orderid: str, sku: str, qty: int, uow: unit_of_work.AbstractUnitOfWork) -> str:
#     line = model.OrderLine(orderid, sku, qty)
#     with uow:
#         product = uow.products.get(sku=line.sku)
#         if product is None:
#             raise InvalidSku(f'Invalid sku {line.sku}')
#         batchref = product.allocate(line)
#         uow.commit()
#         return batchref


def deallocate(orderid: str, sku: str, qty: int, batch_ref, uow: unit_of_work.AbstractUnitOfWork) -> str:
    line = model.OrderLine(orderid, sku, qty)
    with uow:
        product = uow.products.get(sku=sku)
        if product is None:
            raise InvalidSku(f'Invalid sku {line.sku}')
        batchref = product.deallocate(line)
        uow.commit()
        return batchref