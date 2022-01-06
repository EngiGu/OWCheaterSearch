from sanic import Sanic
from sanic.response import json as sanic_json
from threading import Thread

from config import Config
from core.model import QueryModel
from core.schema import SESSION
from cheater_eye import CheaterEye

app = Sanic(__name__)


# Thread(target=CheaterEye(logger).start).start()


def msg(data, code=0, msg='ok!'):
    return sanic_json({'code': code, 'msg': msg, 'data': data})


app.static('/', './static/index.html')
app.static('/static', './static/static')
app.static('/favicon.ico', './static/favicon.ico')


@app.middleware('response')
async def session_close(request, response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    if SESSION:
        SESSION.close()


@app.route("/api/total_status", methods=['GET'])
async def total_status(request):
    total, last_pub_time, url_obj = QueryModel.get_total_status()
    data = {
        'total': total,
        'last_pub_time': last_pub_time.strftime("%Y-%m-%d"),
        '_last_pub_time': last_pub_time,
        'title': url_obj.title,
        'url': url_obj.url,
    }
    return msg(data=data)


# @app.route("/api/last_pub_time_cheaters/<stmp:int>", methods=['GET'])
# async def last_pub_time_cheaters(request, stmp):
#     stmp = time.strftime("%Y-%m-%d", time.localtime(stmp))
#     cheaters = QueryModel.get_last_pub_time_cheaters(stmp)
#     data = [Utils.row2dict(i) for i in cheaters]
#     return msg(data=data)


@app.route("/api/cheaters", methods=['GET'])
async def cheaters(request):
    key = request.args.get('key', '*')
    cheaters = QueryModel.get_cheaters(str(key))
    return msg(data=cheaters)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.API_SERVER_PORT, workers=Config.API_SERVER_WORKERS)
