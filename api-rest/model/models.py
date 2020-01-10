from sqlalchemy import Column, Integer, String, Text
from config import ma, db
from model.shared import BaseData
from sqlalchemy import func, and_


#####################
#     Paste         #
#####################


class Paste(db.Model):
    __tablename__ = 'paste'
    id = Column(Integer, primary_key=True)
    key = Column(String(9))
    scrape_url = Column(String(75))
    full_url = Column(String(29))
    size = Column(Integer)
    title = Column(String(255))
    syntax = Column(String(20))
    file_path = Column(String(75))
    username = Column(String(45))
    hits = Column(Integer)
    date = Column(Integer)
    expire = Column(Integer)
    positive = Column(Integer)


class PasteSchema(ma.ModelSchema):
    class Meta:
        model = Paste
        sqla_session = db.session


class PasteData(BaseData):
    def __init__(self):
        super().__init__(Paste)

    def get_page(self, p_num=1, p_size=10, order_by='id', order='asc', filters=''):

        # Base query
        query = self.model.query
        query = query.filter(Paste.positive == 1)
        # Apply filter if necessary
        if filters and filters != '':
            query = query.filter(self.model.key.like('%{}%'.format(filters)))
        # Apply order
        if order != 'asc' and order != 'desc':
            order = 'asc'
        order_func = getattr(getattr(self.model, order_by, self.model.id), order)
        query = query.order_by(order_func())
        # Return the page and the count of the data.
        return query.paginate(p_num, p_size, False).items, query.count()

    def get_previous_id(self, id_item):
        return db.session.query(func.max(self.model.id)).filter(self.model.id < id_item).filter(Paste.positive == 1).first()[0]

    def get_next_id(self, id_item):
        return db.session.query(func.min(self.model.id)).filter(self.model.id > id_item).filter(Paste.positive == 1).first()[0]


#####################
#        Hit        #
#####################

class Hit(db.Model):
    __tablename_ = 'hit'
    id = Column(Integer, primary_key=True)
    entity = Column(String)
    source_type = Column(String)
    source_id = Column(Integer)
    value = Column(Text)
    process = Column(Integer)


class HitSchema(ma.ModelSchema):
    class Meta:
        model = Hit
        sqla_session = db.session


class HitData(BaseData):
    def __init__(self):
        super().__init__(Hit)

