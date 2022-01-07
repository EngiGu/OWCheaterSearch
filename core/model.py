import datetime
from sqlalchemy import func

from config import Config
from core.schema import Urls, Cheaters, SESSION
from core.utils import Utils
from core.status import UrlStatus


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
        x = 1000
        n_datas = [datas[i:i + x] for i in range(0, len(datas), x)]

        for n_data in n_datas:
            sql = """INSERT INTO `ow_cheaters` (%s) VALUES %s ON DUPLICATE KEY UPDATE %s"""
            fields = ['full_name', 'name', 'blizzard_id', 'url_id', 'status', 'created', 'pub_time']
            fields_statement = ', '.join([f'`{f}`' for f in fields])
            fields_values = ', '.join([f'{f}=VALUES({f})' for f in fields])
            values = ', '.join([
                f'({", ".join([CrawlerModel.str(data.get(f, "")) for f in fields])})'
                for data in n_data
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

    @staticmethod
    def change_url_status(u_id, status):
        obj = SESSION.query(Urls).filter(
            Urls.id == u_id
        ).first()
        obj.status = status
        SESSION.commit()


class QueryModel:
    @staticmethod
    def get_total_status():
        total = SESSION.query(func.count(Cheaters.id)).scalar()
        last_pub_time, url_obj = SESSION.query(Cheaters.pub_time, Urls).join(
            Urls,
            Urls.id == Cheaters.url_id
        ).group_by(
            Cheaters.pub_time
        ).order_by(
            Cheaters.pub_time.desc()
        ).limit(1).first()
        return total, last_pub_time, url_obj

    @staticmethod
    def get_last_pub_time_cheaters(self, pub_time):
        return SESSION.query(Cheaters).filter(
            Cheaters.pub_time >= '%s 00:00:00' % pub_time,
            Cheaters.pub_time <= '%s 23:59:59' % pub_time,
        ).limit(100).all()

    @staticmethod
    def get_cheaters(key):
        chs_urls = SESSION.query(Cheaters, Urls).join(
            Urls,
            Urls.id == Cheaters.url_id
        )
        if key != '*':
            chs_urls = chs_urls.filter(
                Cheaters.full_name.like('%' + key + '%')
            )
        chs_urls = chs_urls.order_by(
            Cheaters.pub_time.desc()
        ).limit(Config.PAGE_LIMIT).all()

        return QueryModel.format_cheater(chs_urls)

    @staticmethod
    def format_cheater(chs_urls):
        r = []
        for ch, url in chs_urls:
            one = Utils.row2dict(ch)
            one['source_title'] = url.title
            one['source'] = url.url
            r.append(one)
        return r
