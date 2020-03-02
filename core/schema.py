from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR, DATETIME, func, or_, and_, distinct, TIMESTAMP, text, String
from contextlib import contextmanager

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
from core.utils import is_online_server

Base = declarative_base()


class Cheaters(Base):
    __tablename__ = "ow_cheater"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), server_default=text("''"))
    b_id = Column(String(64), server_default=text("''"))  # 战网id
    u_id = Column(Integer, nullable=False)  # url id

    status = Column(Integer, nullable=False, server_default=text("0"))
    created = Column(TIMESTAMP, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    modified = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    def format_name(self):
        return '%s#%s' % (self.name, self.b_id)


class Urls(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(128), server_default=text("''"))
    title = Column(String(64), server_default=text("''"))

    status = Column(Integer, nullable=False, server_default=text("0"))
    created = Column(TIMESTAMP, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    modified = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


online_host = 'ten.sooko.club'
if is_online_server(online_host):
    engine = create_engine(Config.SQLITE_URI.replace(online_host, '127.0.0.1'))
else:
    engine = create_engine(Config.SQLITE_URI)

engine = create_engine(Config.SQLITE_URI, echo=False)
session = sessionmaker(bind=engine)
SessionType = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))


def GetSession():
    return SessionType()


@contextmanager
def session_scope():
    session = GetSession()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


# def init_sqlite():
#     # 谨慎调用，会直接删除已有db文件
#     path = Config.SQLITE_URI.split('sqlite:///')[-1]
#     db_path = '/'.join(path.split('/')[:-1])
#     if os.path.exists(path):
#         os.remove(path)
#     else:
#         if not os.path.exists(db_path):
#             os.makedirs(db_path)
#     Base.metadata.create_all(engine)


if __name__ == "__main__":
    # init_sqlite()
    Base.metadata.create_all(engine)
    pass
