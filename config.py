


class Config:


    API_SERVER_WORKERS = 4
    
    API_SERVER_PORT = 9901
    # sqlite 数据库路径
    SQL_URI = 'mysql+pymysql://root:Gq19940507+****+@cd.sooko.ltd:33066/ow_cheaters'
    # SQLITE_URI = 'mysql+pymysql://root:Gq19940507+****+@172.17.0.1:33066/ow_cheater'

    INTETVER_TIME = 0.1 * 60

    # 入口网址
    EYE_ENTER_URLS = [
        'http://bbs.ow.blizzard.cn/forum.php?mod=forumdisplay&fid=38',
        # 'http://bbs.ow.blizzard.cn/forum.php?mod=viewthread&tid=786840&extra=page%3D1',
        # 'http://bbs.ow.blizzard.cn/forum.php?mod=viewthread&tid=619963&extra=page%3D1'
    ]
