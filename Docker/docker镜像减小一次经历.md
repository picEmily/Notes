# pytorch docker 镜像体积减小/时间减短
参考： 
https://www.infoq.cn/article/3-simple-tricks-for-smaller-docker-images
参考方法中多个stage原理上来讲有好处，但是我测试的用处不大

**本项目涉及到许多来源造成了镜像巨大**
- 预装pytorch和其依赖的linux基础镜像
- 有需要git clone别的包来本地安装，涉及到依赖版本不一样的问题
- 需要apt-get安装redis


**基本思路**
- 先写一个能用的
    - ``COPY``尽量放后面，因为``COPY``要是哪里改了一点是不能用cache的
    - 记得换源，apt-get换源改source.list文件，pip直接加``-i``方便一点
	- 个人感觉一开始debug的时候可以把每层都分开，例如RUN每次只写一个命令，一来方便用cache，二来方便看哪一层比较大
	- 我更习惯用``ENTRYPOINT``(有些人``CMD``)，注意需要了解自己的基础镜像是否有bash，不然shebang写``!#/bin/bash``运行不了。另运行文件要``chmod +x``
- ``docker history [repo:tag]``分析哪一层有优化空间
	- 一是哪些``RUN``可以合并，减少镜像构建次数（``COPY``、``ADD``和``RUN``语句都会在镜像中新建一层。）
	- 二是哪些比较大，然后想办法减小。主要减小思路是去掉cache，去掉不需要的东西

## 优化
### apt-get
- ``apt-get update``超时：用``apt-get -o Acquire::Check-Valid-Until=false update`` 参考：https://manpages.debian.org/testing/apt/sources.list.5.en.html
- 安装完了东西以后``apt-get clean``

### pip
几个可以用来加速/减小体积的option
- ``--no-deps``
- ``--ignore-installed``
- ``--no-cache-dir`` 

因为git clone下来的包经常有很多重复的依赖，导致有的依赖要装好几遍，且版本不一样，有缓存等问题，可能会造成体积变大（一定会造成时间变长）

所以，对于git clone的包都用``pip install --no-deps --ignore-installed --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple .``来安装。这样不会重复地装依赖，且没有cache。另外，安装完成以后删除包节省空间。

对于``requirements``，用``pip install --no-cache-dir --no-deps -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt``，这个是我用``pip freeze``导出的依赖，所有要用的都会在里面的，所以不要``--ignore-installed``

## 例子
```python3
FROM harbor.shannonai.com/public/inf-pytorch:v0.0.1

MAINTAINER ziqi_wang@shannonai.com

WORKDIR /home/work

ENV GIT_SSL_NO_VERIFY=1

# Ali apt-get source.list
ADD ./sources.list /etc/apt

RUN apt-get -o Acquire::Check-Valid-Until=false update && apt-get install -y redis-server && apt-get clean

# install supporting packages
RUN cd .. \
    && git clone https://wangziqi:CWHV7b7P@git.shannonai.com/nlp/allennlp \
    && cd allennlp && git checkout spell_check \
    && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -e .\
    && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple torch==1.1.0 \
    && pip install --no-cache-dir -i https://pypi.shannonai.com/root/dev/+simple/ --trusted-host pypi.shannonai.com nlpc \
    && cd .. \
    && git clone https://wangziqi:CWHV7b7P@git.shannonai.com/liuxin/service_streamer.git \
    && cd service_streamer && pip install -e .

COPY requirements.txt ./
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

COPY boot.sh ./
COPY ifluent_chinese ifluent_chinese
COPY gpu_worker gpu_worker
COPY backend backend
# COPY conf conf
COPY config.py ./

RUN chmod +x ./boot.sh ./backend/wsgi.py ./gpu_worker/gpu_worker.py

EXPOSE 8097

ENTRYPOINT ["./boot.sh"]
```

# Cheetsheet
```
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

# 查看镜像build过程
docker history hello:latest
```