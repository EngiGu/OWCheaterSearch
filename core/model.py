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

            url_obj = Urls(url=url, title=title,
                           created=Utils.now(return_datetime=False))
            s.add(url_obj)
            return url_obj

    def add_one_cheater(self, name, b_id, u_id, pub_time):
        with session_scope() as s:
            ch_ex = self.get_one_cheater(name, b_id)
            if not ch_ex:
                ch = Cheaters(name=name, b_id=b_id, u_id=u_id, created=Utils.now(
                    return_datetime=False), pub_time=pub_time)
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

    # api

    def get_total_status(self):
        with session_scope() as s:
            total = s.query(func.count(Cheaters.id)).scalar()

            last_pub_time, url_obj = s.query(Cheaters.pub_time, Urls).join(
                Urls,
                Urls.id == Cheaters.u_id
            ).group_by(
                Cheaters.pub_time
            ).order_by(
                Cheaters.pub_time.desc()
            ).limit(1).first()
            # print(total, last_pub_time, url_obj)
            return total, last_pub_time, url_obj

    def get_last_pub_time_cheaters(self, pub_time):
        with session_scope() as s:
            return s.query(Cheaters).filter(
                Cheaters.pub_time >= '%s 00:00:00' % pub_time,
                Cheaters.pub_time <= '%s 23:59:59' % pub_time,
            ).limit(100).all()
