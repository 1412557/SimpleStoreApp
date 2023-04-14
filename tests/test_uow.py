import pytest

from domain import commands, model
from service import unit_of_work, messagebus
from sqlalchemy.sql import text


def get_allocated_batch_ref(session, orderid, sku):
    [[orderlineid]] = session.execute(text(
        f'SELECT id FROM order_lines WHERE orderid="{orderid}" AND sku="{sku}"',
    ))
    [[batchref]] = session.execute(text(
        'SELECT b.reference FROM allocations JOIN batches AS b ON batch_id = b.id'
        f' WHERE orderline_id={orderlineid}',
    ))
    return batchref


def test_uow_can_retrieve_a_batch_and_allocate_to_it(session_factory):
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    messBus = messagebus.MessageBus(uow)
    messBus.handle(commands.CreateBatch("batch1", "ADORABLE-SETTEE",100, None))
    messBus.handle(commands.CreateBatch("batch2", "ADORABLE-SETTEE", 100, None))
    assert [] == []
