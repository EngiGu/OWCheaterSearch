import hashlib
import base64
import time
from sanic import Sanic
from sanic.response import json as sanic_json
from sanic import response

from config import Config
from core.model import SQLiteModel
from core.utils import Utils

app = Sanic(__name__)
SQLITE_MODEL = SQLiteModel()


def msg(code=0, msg='ok!', data=''):
    return sanic_json({'code': code, 'msg': msg, 'data': data})


@app.route('/')
async def handle_request(request):
    return await response.file('static/index.html')


@app.route('/favicon.ico')
async def handle_request(request):
    return await response.file('static/favicon.ico')


@app.route("/api/total_status", methods=['GET'])
async def upload(request):
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
async def upload(request, stmp):
    stmp = time.strftime("%Y-%m-%d", time.localtime(stmp))
    cheaters = SQLITE_MODEL.get_last_pub_time_cheaters(stmp)
    data = [Utils.row2dict(i) for i in cheaters]
    return msg(data=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.API_SERVER_PORT,
            workers=Config.API_SERVER_WORKERS)
