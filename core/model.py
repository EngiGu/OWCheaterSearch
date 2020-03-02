from sqlalchemy import func
from core.schema import Urls, Cheaters, session_scope
from core.utils import Utils
from core.status import UrlStatus


class SQLiteModel:
    pass

    def get_one_url(self, url):
        with session_scope() as s:
            return s.query(Urls).filter(
                Urls.url == url
            ).first()

    def add_one_url(self, url, title):
        with session_scope() as s:
            url_obj = self.get_one_url(url)
            if url_obj:
                return url_obj

            url_obj = Urls(url=url, title=title, created=Utils.now(return_datetime=False))
            s.add(url_obj)
            return url_obj

    def add_one_cheater(self, name, b_id, u_id, pub_time):
        with session_scope() as s:
            ch_ex = self.get_one_cheater(name, b_id)
            if not ch_ex:
                ch = Cheaters(name=name, b_id=b_id, u_id=u_id, created=Utils.now(return_datetime=False), pub_time=pub_time)
                s.add(ch)
                return ch
            return ch_ex

    def get_one_cheater(self, name, b_id):
        with session_scope() as s:
            return s.query(Cheaters).filter(
                Cheaters.name == name,
                Cheaters.b_id == b_id
            ).first()

    def change_one_url_status(self, u_id, status):
        with session_scope() as s:
            obj = s.query(Urls).filter(
                Urls.id == u_id
            ).first()
            obj.status = status
            s.flush()

