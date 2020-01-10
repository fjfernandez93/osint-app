from config import db
from sqlalchemy import func, and_

class BaseData:
    def __init__(self, model):
        self.model = model
        self.columns = [c.name for c in self.model.__table__.columns]

    @staticmethod
    def commit():
        db.session.commit()

    def get_all(self):
        return self.model.query.all()

    def get_page(self, p_num=1, p_size=10, order_by='id', order='asc', filters=''):

        # Base query
        query = self.model.query
        # Apply filter if necessary
        if filter and filter != '':
            query = query.filter(self.model.key.like('%{}%'.format(filters)))
        # Apply order
        if order != 'asc' and order != 'desc':
            order = 'asc'
        order_func = getattr(getattr(self.model, order_by, self.model.id), order)
        query = query.order_by(order_func())
        # Return the page and the count of the data.
        return query.paginate(p_num, p_size, False).items, query.count()

    def get_total_count(self):
        return self.model.query.count()

    def get_by(self, **kwargs):
        for key in kwargs.copy().keys():
            if key not in self.columns:
                del kwargs[key]
        return self.model.query.filter_by(**kwargs).all()

    def get_by_id(self, id_item):
        return self.model.query.get(id_item)

    def get_previous_id(self, id_item):
        return db.session.query(func.max(self.model.id)).filter(self.model.id < id_item).first()[0]

    def get_next_id(self, id_item):
        return db.session.query(func.min(self.model.id)).filter(self.model.id > id_item).first()[0]

    def test(self):
        a = self.model
        pass