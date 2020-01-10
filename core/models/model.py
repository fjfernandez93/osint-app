from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
Base = declarative_base()


class Paste(Base):
    __tablename__ = "paste"
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
    date_inserted = Column(DateTime, server_default=func.now())


class Hit(Base):
    __tablename__ = "hit"
    id = Column(Integer, primary_key=True)
    entity = Column(String(20))
    source_type = Column(String(20))
    source_id = Column(Integer)
    value = Column(String(256))
    process = Column(Integer)


class BaseData:

    def __init__(self, session, model):
        self.model = model
        self.attributes = [x for x in self.model.__dict__.keys() if not x.startswith('_')]
        self.session = session

    def commit(self):
        self.session.commit()

    def add(self, obj):
        self.session.add(obj)
        self.session.commit()

    def get_by(self, **kwargs):
        for key in kwargs.copy().keys():
            if key not in self.attributes:
                del kwargs[key]
        return self.session.query(self.model).filter_by(**kwargs).all()


class PasteData(BaseData):

    def __init__(self, session):
        super().__init__(session, Paste)


class HitData(BaseData):

    def __init__(self, session):
        super().__init__(session, Hit)
