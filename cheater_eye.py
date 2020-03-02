
import re
import time
import requests

from core.model import SQLiteModel, session_scope
from core.status import UrlStatus
from config import Config


SQLMODEL = SQLiteModel()


class CheaterEye:
    def __init__(self, logger):
        self.logger = logger
        self.first_run = True

    def send_request(self, url):
        kwargs = {
            'url': url,
            'timeout': 30,
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
            }
        }
        return requests.get(**kwargs).content.decode()

    def _enter_url_check_rules(self, ps):
        # 入口网址的校验
        result = re.findall(r'<a href="(.*?)" .*?>(.*?)</a>', ps, re.S)
        r = []
        for url, title in result:
            if '处罚' in title:
                r.append((url, title))
        return r

    def extract_detail_names(self, ps, title):
        # 提取id
        names = re.findall(r'<li>(\w+#\d+)</li>', ps, re.S)
        # print(names)
        if names:
            pub_time = re.findall(r'<!-- 发表于  -->(.*?)</p>', ps, re.S)
            # 日期修正
            m_d = re.findall(r'(\d+)月(\d+)日', title, re.S)
            # print('m d', m_d)
            if m_d:
                year = pub_time[-1].split('-')[0]
                pub_time = '%s-%s-%s 00:00:00' % (year, m_d[0][0], m_d[0][1])
            else:
                pub_time = pub_time[0]
            pub_time = pub_time.replace('<span title="', '')
            # print(pub_time)
            return pub_time, names
        return '', []

    def deal_detail_names(self, url, title, pub_time, names):
        if names:
            url_obj = SQLMODEL.add_one_url(url, title)
            for _name_ in names:
                name, b_id = _name_.split('#')
                SQLMODEL.add_one_cheater(name, b_id, url_obj.id, pub_time)
                self.logger.info('added %s#%s \t\t pub_time: %s', name, b_id, pub_time)
            
            # 更改状态，不会再次爬取这个网址
            with session_scope() as s:
                url_obj.status = UrlStatus.execed
                s.flush()

            pass
        
    def watch_enter_url(self, url):
        # 监控入口网址里面是否有新的名单网址加入进来
        page_source = self.send_request(url)
        new_urls = self._enter_url_check_rules(page_source)
        if new_urls:
            self.logger.info('detect new url, start update....')
            # 处理一个新的带名单的网址
            return_new_urls = []
            for url, title in new_urls:
                # url = 'http://bbs.ow.blizzard.cn/%s' % url
                url = url.replace('&amp;', '&')
                if 'bbs.ow.blizzard.cn' not in url:
                    url = 'http://bbs.ow.blizzard.cn/%s' % url
                print(url, title)
                return_new_urls.append(url)

                url_obj = SQLMODEL.get_one_url(url)
                if url_obj and url_obj.status == UrlStatus.execed:
                    self.logger.info('url has crwaled, url: %s', url)
                else:
                    detail_page = self.send_request(url)
                    pub_time, names = self.extract_detail_names(detail_page, title)

                    self.deal_detail_names(url, title, pub_time, names)

            return return_new_urls

    def start(self):
        # 1. 监控入口网址变化
        while True:
            try:
                for url in Config.EYE_ENTER_URLS:
                    new_urls = self.watch_enter_url(url)
                # 2. 如果变化进入口网址， 存储信息
                if self.first_run:
                    Config.EYE_ENTER_URLS = Config.EYE_ENTER_URLS + new_urls
                    self.first_run = False
            except Exception as e:
                self.logger.exception(e)
            self.logger.info('eye sleep %ss', Config.INTETVER_TIME)
            time.sleep(Config.INTETVER_TIME)


if __name__ == "__main__":
    import logging
    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s - %(message)s')
    ce = CheaterEye(logger=logging.getLogger(__name__))
    ce.start()
