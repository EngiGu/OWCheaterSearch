# ow_cheater_search

![image](https://engigu.coding.net/p/imagestore/d/imagestore/git/raw/back/store/3f766b0c18c63c57a15904db037fc61f.png)

玩游戏最痛恨的就是开g的，自己有时间玩的
主要是爬取守望先锋的社区所有封号帖子，并监控新帖子录入
支持搜索，后期可能支持订阅推送


# 环境
 -  python3.7.2
 -  sainc
 -  mysql

# 运行
推荐使用`docker-compose`
1. 先 `cp config.py.sample config.py`，更改`mysql`配置
2. `docker-compose up --build`
2. 访问`9901`端口

# TODO
 - 可能支持订阅
 - 可能不会再次更新