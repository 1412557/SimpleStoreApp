from domain import events
from domain.model import Batch, Product, OrderLine
from datetime import datetime

today = datetime.today()


def test_records_out_of_stock_event_if_cannot_allocate():
    batch = Batch('batch1', 'SMALL-FORK', 10, eta=today)
    product = Product(sku="SMALL-FORK", batches=[batch])
    product.allocate(OrderLine('order1', 'SMALL-FORK', 10))
    allocation = product.allocate(OrderLine('order2', 'SMALLFORK', 1))
    assert product.events[-1] == events.OutOfStock(sku="SMALLFORK")
    assert allocation is None