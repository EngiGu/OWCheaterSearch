#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : install.py
# @Author: guq  
# @Date  : 2022/1/6
# @Desc  :

from sqlalchemy import create_engine
from core.schema import Base
from config import Config


def install_db():
    engine = create_engine(Config.SQL_URI, echo=True)
    Base.metadata.create_all(engine)
    print('create db completed.')


if __name__ == '__main__':
    install_db()
