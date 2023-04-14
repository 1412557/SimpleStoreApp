import abc
import logging

from sqlalchemy.exc import NoResultFound

from adapters import orm
from domain import model


class AbstractRepository(abc.ABC):

    def __init__(self):
        self.seen = set()

    def add(self, product: model.Product):
        self._add(product)
        self.seen.add(product)

    def get(self, sku) -> model.Product:
        product = self._get(sku)
        if product:
            self.seen.add(product.fill_event())
        return product

    def get_by_batchref(self, batchref) -> model.Product:
        product = self._get_by_batchref(batchref)
        if product:
            self.seen.add(product)
        return product

    @abc.abstractmethod
    def _add(self, product: model.Product):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, sku) -> model.Product:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> [model.Product]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_batchref(self, batchref) -> model.Product:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, product):
        self.session.add(product)

    def _get(self, sku):
        try:
            logging.info(sku, type(sku))
            return self.session.query(model.Product).filter_by(sku=sku).one()
        except NoResultFound:
            return None

    def _get_by_batchref(self, batchref):
        return self.session.query(model.Product).join(model.Batch).filter(orm.batches.c.reference == batchref,).first()

    def list(self):
        return self.session.query(model.Product).all()


# class ProductRepository(AbstractRepository):
#
#     def __init__(self, products):
#         super().__init__()
#         self._products = set(products)
#
#     def add(self, product):
#         self._products.add(product)
#
#     def get(self, sku):
#         try:
#             p = next(p for p in self._products if p.sku == sku)
#         except StopIteration:
#             return None
#         return p
#
#     def list(self):
#         return list(self._products)