import datetime
import os

from sqlalchemy import TIMESTAMP


class Utils:

    @staticmethod
    def now(return_datetime=False):
        if not return_datetime:
            return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return datetime.datetime.now()

    @staticmethod
    def run_in_docker():
        return bool(os.environ.get('RUN_IN_DOCKER'))

    @staticmethod
    def row2dict(row):
        def convert_datetime(value):
            if value:
                return value.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return ""

        d = {}
        for col in row.__table__.columns:
            if isinstance(col.type, TIMESTAMP):
                value = convert_datetime(getattr(row, col.name))
            else:
                value = getattr(row, col.name)
            d[col.name] = value
        return d


import socket
import requests


def SynResolve(host):
    try:
        results = socket.getaddrinfo(host, None)
        for result in results:
            return result[4][0]
    except Exception as e:
        print(e)


def is_online_server(host):
    res = requests.get('http://pv.sohu.com/cityjson?ie=utf-8').content.decode()
    if SynResolve(host) in res:
        return True
    return False


if __name__ == '__main__':
    print(Utils.now())
    pass
