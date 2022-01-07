import os


class Config:
    API_SERVER_WORKERS = os.environ.get('WORKS', 4)

    API_SERVER_PORT = os.environ.get('PORT', 9901)
    # sqlite 数据库路径
    SQL_URI = 'mysql+pymysql://root:Gq19940507+****+@172.17.0.1:33066/ow_cheaters'
    # SQLITE_URI = 'mysql+pymysql://root:Gq19940507+****+@172.17.0.1:33066/ow_cheater'

    PAGE_LIMIT = os.environ.get('PAGE_LIMIT', 50)
