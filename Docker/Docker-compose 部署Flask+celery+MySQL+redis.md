# Docker-compose 部署Flask + celery + MySQL + redis
## 部署web app要求
- virtualenv 隔离环境
- gunicorn配置（用来在服务器上部署python 后台服务（支持大多数框架））
- Dockerfile打包server镜像？
- docker-compose 配置server和mysql镜像

ubuntu 18 lts
## Prerequisite
- MySQL基本操作(CRUD)
- Redis基本操作
- Docker基本知识(官方文档前三章足够应付此项目)

# 部署步骤
本项目使用docker-compose来构建一个Flask+celery+MySQL+redis多个容器的服务。有好几个服务需要搞在一起的时候用docker-compose方法会比较容易一点。image主要是三个部分：

- flask web app(包含celery)
- MySQL服务
- Redis服务

其中，MySQL和redis可以用官方的镜像（直接pull image，不需要自己写Dockerfile），自己的flask web app需要自己写Dockerfile，然后在*docker-compose.yml* 里面build（当然也可以先用``docker build .``，然后再在*docker-compose.yml* 里面pull他的image）。需要注意的地方：

- 怎么写Dockerfile，*docker-compose.yml*文件
- 不同服务的启动顺序，怎么实现
- 怎么把不同的服务联系起来（例如本地连接MySQL就用``username:password@localhost:3306``）

## 文件夹结构
```
├── app2
│   ├── app.db
│   ├── buildDB.py
│   ├── celery_worker.py
│   ├── extensions
│   ├── forms
│   ├── __init__.py
│   ├── models
│   ├── routes
│   ├── settings.py
│   ├── static
│   ├── tasks
│   ├── templates
│   └── upload
├── app.py
├── boot.sh
├── docker-compose.yml
├── Dockerfile
├── mysql
│   └── init_mysql.sql
├── path.pth
├── README.md
├── requirements.txt
├── tests
│   └── test_basics.py
└── venv
    ├── bin
    ├── include
    ├── lib
    └── share
```

## Dockerfile
这个项目中唯一需要写Dockerfile的就是我们的Flask web app， 这里的Dockerfile的几个作用：

- 创建一个flask app的image(python+flask_web_app)及其container到docker上
- 安装虚拟环境venv，安装必要的lib
- 启动celery，启动flask app

```
# Dockerfile

FROM python:3.6-alpine

WORKDIR /app

COPY requirements.txt ./
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY app2 app2
COPY app.py ./
COPY boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP app.py
ENV FLASK_ENV=development

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
```

```
# boot.sh

#!/bin/sh
source venv/bin/activate
venv/bin/celery worker --app=app2.celery_worker.celery --loglevel=info -D
exec gunicorn -b :5000 --access-logfile - --error-logfile - app:app
```

**解释**
- 这里的flask web app 运行在python3.6-alpine中，先搞一个python的镜像
- docker中的app将运行在 /app/文件夹中
- ``COPY``: 命令复制当前主机文件夹的东西到docker中
- ``RUN``: 运行命令，这里运行的是：
	- 创建venv
	- 在venv中安装requirements
	- 安装gunicorn pymysql（大概是一个运行web的服务器之类的）
- ``ENV``: 指定运行的环境（这两个环境我就用的在我自己的电脑上跑的时候用的）
- ``EXPOSE``：指定这个docker暴露给别人的端口是5000（？？？不知道细节）
- boot.sh 在这里启动了venv，启动了celery worker，flask app（为了好改分开写了一个文件），``exec`` 的作用大概是把web app绑在主线程上，关container的时候才会关（？？？不确定）；``gunicorn``的最后一个参数指的是docker中的/app/app.py

## docker-compose.yml
```
## docker-compose.yml

version: "3"
services:
  mysql:
    hostname: mysql
    image: "mysql/mysql-server:5.7"
    environment:
      MYSQL_ROOT_PASSWORD: admin
    restart: unless-stopped
    volumes:
      - "./mysql:/docker-entrypoint-initdb.d"

  redis:
    hostname: redis
    image: redis
    command: redis-server
  
  app:
    build:
      context: .
      dockerfile: Dockerfile
    depends_on:
      - redis
      - mysql
    ports:
    - "5000:5000"
```

**解释**

- 格式抄一下，需要哪些image就写几个
- ``version``不知道为啥都写3，我试过1，会报错
- ``mysql``中
	- ``hostname``: 让我的flask web app连接，*setting.py*中配置``SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://wzq:123456@mysql:3306/WEBSERVICE'``(注意，连接mysql的username,password是我在mysql/init_mysql.sql 中指定的，还有WEBSERVICE这个database也是)
	- ``environment``: 创建image的时候就有一个root用户的密码
	- ``volumes``: 意思是把我电脑里的东西搞到docker里面，可以说命令(*.sql)，可以是数据库的数据（我这里把mysql/init_mysql.sql 搞到docker里面，帮我创建用户(不推荐一直用root用户)，帮我创建WEBSERVICE DATABASE然后在里面创建TABLE）
- ``redis``中
	- ``hostname``: *setting.py*中配置``CELERY_BROKER_URL = 'redis://redis:6379/0'``, ``CELERY_RESULT_BACKEND = 'redis://redis:6379/0'``（我这里有一个小问题，我启动celery的时候没有用setting.py里面的配置的redis，我直接卸载初始化celery的地方了，但是好像再docker这里它用的是setting.py里面的配置）
	- ``command``: 启动redis server
- ``app``
	- ``build``: 根据本文件夹的Dockerfile 来build flask web app；完事以后会看见python和app两个image，以及会有app的container
	- ``depends_on``: 告诉docker我的app depends on mysql和redis（？？？似乎以前是用links）（我之前写的是db: hostname:mysql // depends_on:db  连接不上，不知道为什么，我就把db改成了mysql）
    - ``ports``：[我用localhost上的端口]:[docker暴露的端口(我在Dockerfile的EXPOSE中设的是5000)]，指定了我用来登录ports为0.0.0.0:5000（如果不指定的话不会有0.0.0.0，那么我无法用[http://localhost:5000](http://localhost:5000) 来登录）（redis和MySQL因为是这几个服务之间通信，我不需要进去看，所以没写这个ports）


```
## mysql/init_mysql.sql

create DATABASE WEBSERVICE character set utf8;
CREATE USER 'wzq'@'%' IDENTIFIED BY '123456';
GRANT ALL privileges on WEBSERVICE.* to 'wzq'@'%';

use WEBSERVICE;
CREATE TABLE IF NOT EXISTS `user`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `username` VARCHAR(100) NOT NULL,
   `password` VARCHAR(40) NOT NULL,
   PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `history`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `feature` VARCHAR(1000) NOT NULL,
   `text` VARCHAR(1000) NOT NULL,
   `result` VARCHAR(1000) NOT NULL,
   PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO user
(username, password)
VALUES
("admin", "admin");

```

## up到docker中
- 在terminal 中： ``docker-compose up``
- [http://localhost:5000](http://localhost:5000) 访问我们的flask web app

**调试：**
- 如果想要停止，再开一个terminal：``docker-compose down ``
- 如果修改了web app中的代码：
	- ``docker-compose down `` 停止所有用docker-compose创建的container（但是image都还在）
	- ``docker image ls`` 找到web app的[image id]；然后``docker image rm [image id]``删掉这个image
	- ``docker-compose up`` 再来一次
- 如果修改了Dockerfile：
	- 据说改了某一行，这一行之前的hi用cache，这一行之后的会重新运行一遍
- 改了docker-compose.yml
	- 不知道，我试了一下不会重新建image，所以还是删了image再up一遍
- 如果想看某个服务的log
	- ``docker logs [container id]``
- 如果想操作一下某个服务，比如数据库啥的
	- ``docker exec -it [container id] /bin/sh``
- 如果直接登录MySQL，``docker run --name db -e MYSQL_ROOT_PASSWORD=xxx -d mysql`` // -d 后台运行

# Cheat sheet 
## docker
权限不够每句话都加sudo
```bash
# 查
docker container ls // 只能看到在run的container
docker container ls -a
docker image -ls
docker ps

# biuld
docker build -t [repo:tag] .

# 删除
docker container rm [container id]
docker image rm [image id]
# 删除全部container，image
docker container rm $(sudo docker container ls -a -q)
docker image rm $(sudo docker image ls -a -q)

# 进入某个container的bash
docker exec -it [container id] /bin/sh
# 进入not running的容器
docker run -it my/python:v1 /bin/bash

# docker-compose
docker-compose up 
docker-compose down ## stop and remove all containers in docker-compose.yml file

# 查看历史
docker history hello:latest
```
## MySQL
```
## 进入MySQL·
mysql -u [username] -p [password]
mysql -u root -p

# 创建用户并赋予权限

# 创建database（注意编码设定一下utf-8）

# 创建table（注意编码设定一下utf-8）

# 创建table里面的row

# 操作数据库
show databases;
use [database name];
show tables;

```

## redis
```
## 存储方式; key-value

## 启动redis客户端
redis-cli

## 在客户端中测试连接（连接上会得到PONG）
> ping

## 备份和恢复数据
> SAVE

## 操作key [Command][Key_name]
> SET key value
> GET key
> KEYS pattern 
> KEYS *
```

# FAQ
### ``docker-compose up`` 报错error time out
[https://stackoverflow.com/questions/26861390/docker-run-connection-timeout](https://stackoverflow.com/questions/26861390/docker-run-connection-timeout)
- 关掉小飞机等代理
- 记得换源（docker的源）
- 有的时候重启就好了...

### MySQL可能遇到的问题
- RuntimeError: cryptography is required for sha256_password or caching_sha2_password  
[https://www.cnblogs.com/xieshuang/p/9028362.html](https://www.cnblogs.com/xieshuang/p/9028362.html)
大概就是用MySQL·5.7就好了，新的功能太多难得设置
- 存不进去数据库
	- "Data too long for column 'result' at row 1"
	- 编码可能不对
	- 可能是没和web app连接上，检查一下settings.py,各个地方设置的端口，yml里面设置的hostname

### requirements.txt  
``pip freeze > requirements.txt``

### 编码问题
html，.py文件，mysql，.txt文件都用utf-8就没啥问题了（系统也装上utf-8，一开始我的系统只有英文的utf-8好像，百度一下装上中文的）
  
我还指定了``ENV LANG C.UTF-8``再docker-compose.yml中，不知道有没有用

in head  
<meta charset="utf-8"/>

### server internal error
我遇到过蛮多原因：
- 一开始是mysql没连上
- 还遇到过编码不对（某个地方不是utf-8之类的（比如html，某个txt文件，MySQL））
- 还遇到过某个文件路径不对（改成了绝对路径，注意是再docker里面的绝对路径）

大概的方法就是看app的报错信息，进到redis里面看worker的报错信息来找。

### 各种路径问题
- 用绝对路径
- ``import sys``, ``sys.path.append('..')``之类的
- pycharm的话把每个文件夹都设置为source root
- 用*.pth文件试试

### 查看容器日志  
[https://www.jianshu.com/p/1eb1d1d3f25e](https://www.jianshu.com/p/1eb1d1d3f25e)  
``docker logs CONTAINER_ID``

### http://localhost:5000 登录不上去
- docker-compose.yml
```
## app 要指定ports
## 否则不会0.0.0.0:5000->5000
## 我不能从本地访问
ports:
  - "5000:5000"
```
- 检查一下端口写错没，``docker container ls`` 可以看到ports，要有0.0.0.0:xxxx的才能从localhost访问

