# ImageBed

![image](https://ps.ssl.qhmsg.com/t028f522be60483b180.jpg)
![image](https://ps.ssl.qhmsg.com/t0254198e701f13493f.jpg)
写`Markdown`的时候总是要做图片的引用，使用`github`速度又不是很友好，看到国内代码托管平台`gitee`， 有`openapi`([`gitee`.`swagger`](https://gitee.com/api/v5/swagger))可以调用，于是写了这个基于`仓库`的图床，主要放一些自己文字里的图片。

页面很low，可以只跑api, 后端框架使用`sanic`，自己也是第一次使用这个异步框架。

图片文件名的生成使用文件的`md5值`，使用`sqlite.db`对上传记录进行持久化，并进行上传去重复判断。

现在已经支持国内的`gitee`和`coding`, 适合做博文和文章图片引用，并且会自动存在仓库做保存。

加入一些不用在意质量的免费接口， 平时水图用。

欢迎大家提`issue`

##  Release

 - 2020.02.26 添加百度接口
 - 2020.02.23 添加搜狗接口
 - 2020.02.22 加入多个图源切换，加入其他免费接口
 - 2020.02.10 项目重构，支持coding
 - 2020.02.09 支持剪贴板上传
 - 2020.02.08 支持上传进度显示

## 环境
  - python3.7.2
  - sanic
  - 更多详见`requirements.txt`


## 说明
先拉取项目, `cp config.py.sample config.py` ,更改`config.py`里的配置，修改参见下面的说明
```shell
git clone https://github.com/EngiGu/imagebed.git
```
1. 整个项目一起运行(**推荐**)

    a. 启动命令
    ```shell
    docker-compose build
    docker-compose up -d
    ```
    b. 如果是第一次运行，需要执行初始化(以后不用执行)
    ```shell
    docker-compose exec imagebed-server sh -c 'python init_server.py'
    ```
    c. 启动后访问`ip:9900`端口, 如果需要改动，修改`docker-compose.yml`里的端口

2. 只运行后端`api-server`
    
    a. 打包运行
     ```shell
    docker build -t imagebed-server .
    docker run -d -p 8000:8000 --name imagebed-server imagebed-server
    ```
    如果要把`sqlite`保存在外部，需要挂载`-v {yourpath}:/app/sqlite_db`
    
    b. 如果是第一次运行，需要执行初始化(以后不用执行)
    ```shell
    docker-compose exec imagebed-server sh -c 'python init_server.py'
    ```
    c. 请求参数
    ```curl
    curl -X POST 'http:/ip:8000/api/upload' -d '{file: (binary)}'
    ```

## 配置参数说明

```python
    ############## GITEE配置 ##############
    #  GITEE 用户授权码, 获取请打开 https://gitee.com/profile/personal_access_tokens/new 授权复制出现的access_token
    GITEE_ACCESS_TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxx'
    # OWNER 仓库所属空间地址(企业、组织或个人的用户名)
    GITEE_OWNER = 'owner'
    # repo 仓库名字
    GITEE_REPO = 'repo_name'
    # BRANCH 仓库分支(如果不存在的分支，需要提前建好)
    GITEE_BRANCH = 'branch_name'
    # PATH 分支里的路径(如果要放在一个不存在的路径，最好也提前建好, 如果是根目录写/)
    GITEE_STROE_PATH = 'your/images/path'
    ############## GITEE配置 ##############

    ############## Coding配置 ##############
    # Coding 用户授权码, token获取参见 https://help.coding.net/docs/member/tokens.html
    CODING_ACCESS_TOKEN = 'xxxxx'
    # OWNER 仓库所属空间地址(企业、组织或个人的用户名)
    CODING_OWNER = 'owner'
    # repo 仓库名字
    CODING_REPO = 'repo_name'
    # BRANCH 仓库分支(如果不存在的分支，需要提前建好)
    CODING_BRANCH = 'branch_name'
    # PATH 分支里的路径(如果要放在一个不存在的路径，最好也提前建好, 如果是根目录写/)
    CODING_STROE_PATH = 'your/images/path'
    ############## Coding配置 #############
```


##  大小说明
[官方说明](https://gitee.com/help/articles/4125#article-header0)

![输入图片说明](https://images.gitee.com/uploads/images/2020/0209/160615_555f2669_1346635.png "屏幕截图.png")


## TODO
  - ~~页面优化~~
  - ~~支持剪贴板上传~~
  - 防滥用
  
