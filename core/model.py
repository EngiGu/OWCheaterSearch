import datetime

from sqlalchemy import func, or_
from core.schema import Urls, Cheaters, session_scope, SESSION
from core.utils import Utils
from core.status import UrlStatus


class SQLiteModel:
    pass

    def get_one_url(self, url):
        with session_scope() as s:
            return s.query(Urls).filter(
                Urls.url == url
            ).first()

    def add_one_url(self, url, title, pub_time):
        with session_scope() as s:
            url_obj = self.get_one_url(url)
            if url_obj:
                return url_obj

            url_obj = Urls(
                url=url,
                title=title,
                created=Utils.now(return_datetime=False),
                pub_time=pub_time
            )
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

    def get_cheaters(self, key):
        with session_scope() as s:
            chs_urls = s.query(Cheaters, Urls).join(
                Urls,
                Urls.id == Cheaters.u_id
            )
            if key != '*':
                chs_urls = chs_urls.filter(
                    or_(
                        Cheaters.name.like('%' + key + '%'),
                        Cheaters.b_id.like('%' + key + '%'),
                    )
                )
            chs_urls = chs_urls.order_by(
                Cheaters.pub_time.desc()
            ).limit(50).all()

            return self.format_cheater(chs_urls)

    def format_cheater(self, chs_urls):
        r = []
        for ch, url in chs_urls:
            # print(ch, url)
            one = Utils.row2dict(ch)
            one['b_name'] = ch.format_name()
            one['reason'] = self.format_reason(url.title)
            r.append(one)
        return r

    def format_reason(self, title):
        title = title.replace('《守望先锋》', '')
        sp_1 = title.split('的')[0]
        sp2 = sp_1.split('关于')[-1]
        sp3 = sp2.split('针对')[-1]
        return sp3





class CrawlerModel:
    @staticmethod
    def url_is_crawled(url, title):
        # 是否已经抓过
        # with session_scope() as s:
        url_obj = SESSION.query(Urls).filter(
            Urls.url == url, Urls.status == UrlStatus.execed
        ).first()
        if url_obj:
            return url_obj

        url_obj = Urls(
            url=url,
            title=title,
            created=Utils.now(return_datetime=False),
        )
        SESSION.add(url_obj)
        SESSION.commit()
        return url_obj

    @staticmethod
    def insert_into_names(datas):
        # 插入住区的抓取的名字
        sql = """INSERT INTO `ow_cheaters` (%s) VALUES %s ON DUPLICATE KEY UPDATE %s"""
        fields = ['full_name', 'name', 'blizzard_id', 'url_id', 'status', 'created', 'pub_time']
        fields_statement = ', '.join([f'`{f}`' for f in fields])
        fields_values = ', '.join([f'{f}=VALUES({f})' for f in fields])
        values = ', '.join([
            f'({", ".join([CrawlerModel.str(data.get(f, "")) for f in fields])})'
            for data in datas
        ])
        sql = sql % (fields_statement, values, fields_values)

        SESSION.execute(sql)
        SESSION.commit()

    @staticmethod
    def str(s):
        if isinstance(s, (int, float)):
            return str(s)
        elif isinstance(s, datetime.datetime):
            s = s.strftime('%Y-%m-%d %H:%M:%S')
            return f'"{s}"'
        elif isinstance(s, str):
            return f'"{s}"'
        elif s is None:
            return 'null'
        return f'"{str(s)}"'

    # def get_one_url(self, url):
    #     with session_scope() as s:
    #         return s.query(Urls).filter(
    #             Urls.url == url
    #         ).first()
    #
    # def add_one_url(self, url, title, pub_time):
    #     with session_scope() as s:
    #         url_obj = self.get_one_url(url)
    #         if url_obj:
    #             return url_obj
    #
    #         url_obj = Urls(
    #             url=url,
    #             title=title,
    #             created=Utils.now(return_datetime=False),
    #             pub_time=pub_time
    #         )
    #         s.add(url_obj)
    #         return url_obj
    #
    # def add_one_cheater(self, name, b_id, u_id, pub_time):
    #     with session_scope() as s:
    #         ch_ex = self.get_one_cheater(name, b_id)
    #         if not ch_ex:
    #             ch = Cheaters(name=name, b_id=b_id, u_id=u_id, created=Utils.now(
    #                 return_datetime=False), pub_time=pub_time)
    #             s.add(ch)
    #             return ch
    #         return ch_ex
    #
    # def get_one_cheater(self, name, b_id):
    #     with session_scope() as s:
    #         return s.query(Cheaters).filter(
    #             Cheaters.name == name,
    #             Cheaters.b_id == b_id
    #         ).first()
    #
    @staticmethod
    def change_url_status(u_id, status):
        obj = SESSION.query(Urls).filter(
            Urls.id == u_id
        ).first()
        obj.status = status
        SESSION.commit()
