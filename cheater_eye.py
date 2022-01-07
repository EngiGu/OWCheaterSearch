import datetime
import re
import time
import traceback
import html

import schedule
import requests
from loguru import logger
from lxml import etree

from core.model import CrawlerModel
from core.status import UrlStatus
from core.schema import session_close
from core.utils import Utils

LOGURU_FORMAT = ' '.join(
    (
        '<MMC><bold>[</bold></MMC>' + '<level>{level.name:.1s}</level>',
        '<green>{time:YYMMDD HH:mm:ss.SSS}</green>',
        '<cyan>{name}.{function}:{line}</cyan>' + '<MMC><bold>]</bold></MMC>',
        '<level>{message}</level>',
    )
)
LOGURU_FORMAT = LOGURU_FORMAT.replace('MMC', 'magenta')
logger.add(sys.stderr, colorize=True, format=LOGURU_FORMAT)


class CheaterEye:
    def __init__(self):
        self.start_url = 'http://bbs.ow.blizzard.cn/forum.php?mod=forumdisplay&fid=38'

    def request(self, method='get', **kwargs):
        if 'timeout' not in kwargs:
            kwargs['timeout'] = 10
        kwargs['headers'] = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
        }
        try:
            return getattr(requests, method.lower())(**kwargs)
        except:
            logger.error('request error: %s' % traceback.format_exc())
            return requests.Response()

    def get_all_name_urls(self):
        all_urls = []
        self.get_all_name_urls_by_depth(2, self.start_url, all_urls)
        return all_urls

    def get_all_name_urls_by_depth(self, depth, url, all_urls):
        if depth <= 0:
            return

        page_urls = self._get_url(url)

        all_urls.extend(page_urls)
        depth -= 1

        for page_url, _ in page_urls:
            self.get_all_name_urls_by_depth(depth, page_url, all_urls)

    def _get_url(self, url):
        ps = self.request(**{'url': url}).content.decode()
        result = re.findall(r'<a href="(.*?)" .*?>(.*?)</a>', ps, re.S)
        r = []
        for url, title in result:
            url = html.unescape(url)
            if 'bbs.ow.blizzard.cn' not in url:
                url = 'http://bbs.ow.blizzard.cn/%s' % url
            if '处罚' in title:
                r.append((url, title))
        return r

    def request_page(self, url_obj):
        html_text = self.request(**{'url': url_obj.url}).content.decode()
        tree = etree.HTML(html_text)
        crawled = False
        for node in tree.xpath("//div[@class='post-wrapper']"):
            rst = etree.tostring(node, encoding="utf-8", method="html").decode("utf-8")
            names = re.findall(r'<li>(.*?#\d+)</li>', rst)
            pub_time = re.findall(r'发表于  -->.*?(\d+-\d+-\d+ \d+:\d+:\d+)', rst)
            pub_time = self._format_pub_time(pub_time)
            if names:
                # 匹配到了名字, 插入库
                datas = [
                    {
                        'full_name': name,
                        'name': name.split('#')[0],
                        'blizzard_id': name.split('#')[-1],
                        'url_id': url_obj.id,
                        'status': 1,
                        'created': Utils.now(return_datetime=True),
                        'pub_time': pub_time,
                    }
                    for name in names
                ]
                CrawlerModel.insert_into_names(datas)
                logger.info(f'saved {len(names)} cheaters to db')
                crawled = True

        if crawled:
            CrawlerModel.change_url_status(url_obj.id, UrlStatus.execed)

    def _format_pub_time(self, pub_time):
        # '2022-1-4 15:41:02'
        # 主要还要处理这种格式的时间
        if pub_time:
            pub_time = pub_time[0]
            pt = datetime.datetime.strptime(pub_time, '%Y-%m-%d %H:%M:%S')
            return datetime.datetime.strftime(pt, '%Y-%m-%d %H:%M:%S')
        return ''

    @session_close
    def run(self):
        all_urls = self.get_all_name_urls()
        for url, title in all_urls:
            url = html.unescape(url)
            url_obj = CrawlerModel.url_is_crawled(url, title)
            if url_obj.status == UrlStatus.execed:
                continue
            else:
                logger.info('url created: %s, title: %s' % (url, title))
                self.request_page(url_obj)
                # break


def start_eyes():
    o = CheaterEye()
    o.run()


def eyes_background():
    schedule.every().day.at("00:30").do(start_eyes)
    schedule.every().day.at("08:30").do(start_eyes)
    schedule.every().day.at("12:30").do(start_eyes)
    schedule.every().day.at("16:30").do(start_eyes)
    schedule.every().day.at("20:30").do(start_eyes)
    logger.info('eyes background started')

    while True:
        schedule.run_pending()  # 运行所有可以运行的任务
        time.sleep(1)


if __name__ == '__main__':
    start_eyes()
