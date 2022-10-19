# OWCheaterSearch
![image](https://gitee.com/engigu/imagestore/raw/back/store/45e1cd01eef59fc77899d0cf43fc9b16.png)

守望的封号反馈等于没有，所以写了这个

主要是爬取守望先锋的社区所有封号帖子，并监控新帖子录入

支持搜索，后期可能支持订阅推送

预览地址 [小水管,手下留情](https://app.engigu.cn:88/#/ow)

## 环境
 -  python3.7.2
 -  sainc
 -  mysql

## 运行
推荐使用`docker-compose`
1. 先 `cp config.py.sample config.py`，更改`mysql`配置
2. 第一次运行务必执行（创建数据表）
    ```shell
    python install.py
    ```
3. `docker-compose up --build`
4. 访问`9901`端口

## TODO
 - 可能支持订阅
 - 可能不会再次更新
