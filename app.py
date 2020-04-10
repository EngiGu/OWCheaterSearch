import hashlib
import base64
import time
from sanic import Sanic
from sanic.response import json as sanic_json
from sanic import response
from sanic.log import logger
from threading import Thread

from config import Config
from core.model import SQLiteModel
from core.utils import Utils
from cheater_eye import CheaterEye
from core.dns import dns_resolver


app = Sanic(__name__)
SQLITE_MODEL = SQLiteModel()


Thread(target=CheaterEye(logger).start).start()


def msg(code=0, msg='ok!', data=''):
    return sanic_json({'code': code, 'msg': msg, 'data': data})


app.static('/static', './static/static')


@app.route('/')
async def handle_request(request):
    return await response.file('static/index.html')


@app.route('/favicon.ico')
async def handle_request(request):
    return await response.file('static/favicon.ico')


@app.route("/api/total_status", methods=['GET'])
async def total_status(request):
    total, last_pub_time, url_obj = SQLITE_MODEL.get_total_status()
    data = {
        'total': total,
        'last_pub_time': last_pub_time.strftime("%Y-%m-%d"),
        '_last_pub_time': last_pub_time,
        'title': url_obj.title,
        'url': url_obj.url,
    }
    return msg(data=data)


@app.route("/api/last_pub_time_cheaters/<stmp:int>", methods=['GET'])
async def last_pub_time_cheaters(request, stmp):
    stmp = time.strftime("%Y-%m-%d", time.localtime(stmp))
    cheaters = SQLITE_MODEL.get_last_pub_time_cheaters(stmp)
    data = [Utils.row2dict(i) for i in cheaters]
    return msg(data=data)


@app.route("/api/cheaters/<key>", methods=['GET'])
async def cheaters(request, key):
    cheaters = SQLITE_MODEL.get_cheaters(str(key))
    return msg(data=cheaters)


@app.route("/api/dns/<domain>", methods=['GET'])
async def dns(request, domain):
    value = dns_resolver(domain.strip())
    # return msg(data=value)
    return response.json(
        {'ip': value},
        headers={'X-Served-By': 'sanic', 'Access-Control-Allow-Origin': '*'},
        status=200
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.API_SERVER_PORT,  workers=Config.API_SERVER_WORKERS)
