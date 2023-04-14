from domain import model
from adapters import repository
from sqlalchemy.sql import text

# from domain.model import allocate
# from service import services
# from tests.test_services import FakeSession


# def test_repository_can_save_a_batch(session):
#     # session = sqlite_session_factory()
#     batch = model.Batch("batch1", "RUSTY-SOAPDISH", 100, eta=None)
#     repo = repository.SqlAlchemyRepository(session)
#     repo.add(batch)
#     session.commit()
#     rows = list(session.execute(text(
#         'SELECT reference, sku, _purchased_quantity, eta FROM "batches"'
#     )))
#     assert rows == [("batch1", "RUSTY-SOAPDISH", 100, None)]
#
#
# def insert_order_line(session):
#     session.execute(text(
#         'INSERT INTO order_lines (orderid, sku, qty)'
#         ' VALUES ("order1", "GENERIC-SOFA", 12)'
#     ))
#     [[orderline_id]] = session.execute(text(
#         'SELECT id FROM order_lines WHERE orderid="{}" AND sku="{}"'.format("order1", "GENERIC-SOFA")
#     ))
#     return orderline_id
#
#
# def insert_batch(session, batch_id):
#     session.execute(text(
#         'INSERT INTO batches (reference, sku, _purchased_quantity, eta)'
#         f' VALUES ("{batch_id}", "GENERIC-SOFA", 12,null)'
#     ))
#     [[batch_id1]] = session.execute(text(
#         f'SELECT id FROM batches WHERE reference="{batch_id}" AND sku="GENERIC-SOFA"'
#     ))
#     return batch_id1
#
#
# def insert_allocation(session, orderline_id, batch_id):
#     session.execute(text(
#         'INSERT INTO allocations (batch_id, orderline_id)'
#         f' VALUES ({batch_id}, {orderline_id})'
#     ))
#     [[allocation_id]] = session.execute(text(
#         'SELECT id FROM allocations WHERE batch_id={} AND orderline_id={}'.format(batch_id, orderline_id)
#     ))
#     return allocation_id
#
#
# def test_repository_can_retrieve_a_batch_with_allocations(session):
#     orderline_id = insert_order_line(session)
#     batch1_id = insert_batch(session, "batch1")
#     insert_batch(session, "batch2")
#     insert_allocation(session, orderline_id, batch1_id)
#     repo = repository.SqlAlchemyRepository(session)
#     retrieved = repo.get("batch1")
#     expected = model.Batch("batch1", "GENERIC-SOFA", 100, eta=None)
#     assert retrieved == expected  # Batch.__eq__ only compares reference
#     assert retrieved.sku == expected.sku
#     assert retrieved._purchased_quantity == expected._purchased_quantity
#     assert retrieved._allocations == {
#         model.OrderLine("order1", "GENERIC-SOFA", 12),
#     }
#
# # domain-layer test:
# from datetime import datetime, timedelta
# today = datetime.today()
# tomorrow = today + timedelta(days=1)
# def test_prefers_current_stock_batches_to_shipments():
#     in_stock_batch = model.Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
#     shipment_batch = model.Batch("shipment-batch", "RETRO-CLOCK", 100, eta=tomorrow)
#     line = model.OrderLine("oref", "RETRO-CLOCK", 10)
#     allocate(line, [in_stock_batch, shipment_batch])
#     assert in_stock_batch.available_quantity == 90
#     assert shipment_batch.available_quantity == 100
#
# # service-layer test:
# def test_prefers_warehouse_batches_to_shipments():
#     in_stock_batch = model.Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
#     shipment_batch = model.Batch("shipment-batch", "RETRO-CLOCK", 100, eta=tomorrow)
#     line = model.OrderLine("oref", "RETRO-CLOCK", 10)
#     repo = FakeRepository([in_stock_batch, shipment_batch])
#     session = FakeSession()
#     services.allocate(line, repo, session)
#     assert in_stock_batch.available_quantity == 90
#     assert shipment_batch.available_quantity == 100

def test_product_seen(session):
    repo = repository.SqlAlchemyRepository(session)
    repo.add(model.Product("ADORABLE-SETTEE", batches=[]))
    repo.add(model.Product("HELLO", batches=[]))
    repo.get("HELLO").batches.append()
    assert [] == repo.seen.pop().events
