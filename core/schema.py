from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR, DATETIME, func, or_, and_, distinct, TIMESTAMP, text, String
from config import Config

Base = declarative_base()
engine = create_engine(Config.SQL_URI, echo=False)
session = sessionmaker(bind=engine)
SESSION = session()


class Cheaters(Base):
    __tablename__ = "ow_cheaters"
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(128), server_default=text("''"), unique=True)
    name = Column(String(128), server_default=text("''"))
    blizzard_id = Column(String(64), server_default=text("''"))  # 战网id
    url_id = Column(Integer, nullable=False)  # url id
    status = Column(Integer, nullable=False, server_default=text("0"))
    created = Column(TIMESTAMP, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    pub_time = Column(TIMESTAMP, nullable=False, server_default=text("'0000-00-00 00:00:00'"))

    def format_name(self):
        return '%s#%s' % (self.name, self.blizzard_id)


class Urls(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(128), server_default=text("''"))
    title = Column(String(64), server_default=text("''"))
    status = Column(Integer, nullable=False, server_default=text("0"))
    created = Column(TIMESTAMP, nullable=False, server_default=text("'0000-00-00 00:00:00'"))


def session_close(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        finally:
            if SESSION:
                SESSION.close()

    return wrapper
