# 官方文档笔记
参考：官方文档
https://docs.docker.com/get-started/  

# 为什么使用docker
- 比虚拟技术更高效
	- 启动快
	- 占用硬盘资源少
	- 性能高（内核级）
- 快速搭建环境，保证环境的**一致性**
- **持续**的交付和部署
- 轻松迁移，轻松维护和**扩展**

## part1 Orientation

**一些基本概念：**
- 容器 container：在image中运行的一个或一组应用（可以理解为image的对象）
- 镜像 image：创建docker容器的模板（功能类似虚拟机）（和容器相比可以理解为类）

```bash
## List Docker CLI commands
docker
docker container --help

## Display Docker version and info
docker --version
docker version
docker info

## Execute Docker image
docker run hello-world

## List Docker images
docker image ls

## List Docker containers (running, all, all in quiet mode)
docker container ls
docker container ls --all
docker container ls -aq
```

## part2 Containers
### Structure of apps
- stack: interaction of all services 
- service: how containers behave in production
- containers

### Steps
- define *Dockerfile* , *requirements.txt*
	- the simplist structure of a app to be depoly is: requirements.txt, Dockerfile, app.py
- build: ``docker build --tag=friendlyhello .`` (--tag=[repo]:[tag] // tag is "*latest*" by default)
	- REPOSITORY: friendlyhello; TAG:latest; IMAGE ID: 326387cea398
- run: ``docker run -p 4000:80 friendlyhello``; 
stop: ``docker container stop 1fa4ab2cf395``
- login: ``docker login`` (need to register on the official website first)
- name: ``docker tag [image] [username]/[repository]:[tag]`` (和之前的对比：image id没变， repo变成[username]/[repository]， tag变成[tag])(现在已经注册到Docker’s public registry)
- publish: ``docker push [username]/[repository]:[tag]``
- run from the registry: ``docker run -p 4000:80 username/repository:tag``

**cheat sheet**

```bash
docker build -t friendlyhello .  # Create image using this directory's Dockerfile
docker run -p 4000:80 friendlyhello  # Run "friendlyhello" mapping port 4000 to 80
docker run -d -p 4000:80 friendlyhello         # Same thing, but in detached mode
docker container ls                                # List all running containers
docker container ls -a             # List all containers, even those not running
docker container stop <hash>           # Gracefully stop the specified container
docker container kill <hash>         # Force shutdown of the specified container
docker container rm <hash>        # Remove specified container from this machine
docker container rm $(docker container ls -a -q)         # Remove all containers
docker image ls -a                             # List all images on this machine
docker image rm <image id>            # Remove specified image from this machine
docker image rm $(docker image ls -a -q)   # Remove all images from this machine
docker login             # Log in this CLI session using your Docker credentials
docker tag <image> username/repository:tag  # Tag <image> for upload to registry
docker push username/repository:tag            # Upload tagged image to registry
docker run username/repository:tag                   # Run image from a registry
```

## part3 services
different pieces of the app are called “**services**”
A service only runs one image, but it codifies the way that image runs—what ports it should use, how many replicas of the container should run so the service has the capacity it needs, and so on. 


- already push a image to registry in part2
- define *docker-compose.yml*
- ``docker swarm init``
``docker stack deploy -c docker-compose.yml getstartedlab``
(getstartedlab is the **name** of app
**stack** name: getstartedlab
**service** name: getstartedlab_web
**container** name: getstartedlab_web.1 ~ getstartedlab_web.5)
(now: 1 service stack is running 5 container instances of our deployed image on one host)
- 查看: ``docker service ls ``
- 修改: 修改*docker-compose.yml,*, 然后``docker stack deploy``
- 关闭stack和swarm，``docker stack rm getstartedlab``; ``docker swarm leave --force``

```bash
docker stack ls                                            # List stacks or apps
docker stack deploy -c <composefile> <appname>  # Run the specified Compose file
docker service ls                 # List running services associated with an app
docker service ps <service>                  # List tasks associated with an app
docker inspect <task or container>                   # Inspect task or container
docker container ls -q                                      # List container IDs
docker stack rm <appname>                             # Tear down an application
docker swarm leave --force      # Take down a single node swarm from the manager
```

## part4 swarms
- **swarm**: group of machines that are running docker and they join into a **cluster**
	- each machine is a **node**
	- run commands on **swarm manager **

**create a cluster**
```bash
## create docker-machine
docker-machine create --driver virtualbox myvm1
docker-machine create --driver virtualbox myvm1

docker-machine ls

## INITIALIZE THE SWARM AND ADD NODES
docker-machine ssh myvm1 "docker swarm init --advertise-addr <myvm1 ip>"

## Or, instead of using ssh, we can get the env to use command lines on a machine(recommended)
## docker-machine env <machine>
docker-machine env myvm1
eval $(docker-machine env myvm1)

## deploy the app on the swarm cluster myvm1
docker stack deploy -c docker-compose.yml getstartedlab
```

**cleanup and reboot**

```
docker stack rm getstartedlab

## unset docker-machine env
eval $(docker-machine env -u)

## restart
docker-machine start <machine-name>

```

## part5
## part6

# 常见问题
docker内换源
https://www.aiuai.cn/aifarm299.html

timezone
https://serverfault.com/questions/683605/docker-container-time-timezone-will-not-reflect-changes
https://stackoverflow.com/questions/40234847/docker-timezone-in-ubuntu-16-04-image

# Docker 部署实例
一个部署的实例
参考： https://yq.aliyun.com/articles/691171
https://blog.csdn.net/weixin_33697898/article/details/87213454
**contents:** 
- 访问docker并从中运行程序
- 部署flask应用到docker
- 安装第三方服务（MySql）

## 访问docker
### 安装
windows: 家庭版缺东西 Hyper-V
ubuntu: https://www.runoob.com/docker/ubuntu-docker-install.html

1.更换国内软件源，推荐中国科技大学的源，稳定速度快（可选）

``sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak``
``sudo sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list``
``sudo apt update``
2.安装需要的包

``sudo apt install apt-transport-https ca-certificates software-properties-common curl``
3.添加 GPG 密钥，并添加 Docker-ce 软件源，这里还是以中国科技大学的 Docker-ce 源为例

``curl -fsSL https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu \
$(lsb_release -cs) stable"``
4.添加成功后更新软件包缓存

``sudo apt update``
5.安装 Docker-ce

``sudo apt install docker-ce``
6.设置开机自启动并启动 Docker-ce（安装成功后默认已设置并启动，可忽略）

``sudo systemctl enable docker``
``sudo systemctl start docker``
``sudo systemctl restart docker.service``
7.测试运行

``sudo docker run hello-world``
8.添加当前用户到 docker 用户组，可以不用 sudo 运行 docker（可选）

``sudo groupadd docker``
``sudo usermod -aG docker $USER`` //亲测没啥用，还是得每条命令都``sudo docker xxx``
9.测试添加用户组（可选）

``docker run hello-world``

### 运行程序，查看状态
**run app**
``sudo docker run --name [name] -d -p 8000:5000 --rm [name]:latest``

``--name``选项为新容器提供了一个名称。 
``-d``选项告诉Docker在后台运行容器。 如果没有-d，容器将作为前台应用程序运行，从而阻塞你的命令提示符。 
``-p``选项将容器端口映射到主机端口。 第一个端口是主机上的端口，右边的端口是容器内的端口。 上面的例子暴露了主机端口8000，其对应容器中的端口5000，因此即使内部容器使用5000，你也将在宿主机上访问端口8000来访问应用程序。 
``--rm``选项将使其一旦容器停止就自动被删除。 虽然这不是必需的，但完成或中断的容器通常不再需要，因此可以自动删除。 
最后一个参数是容器使用的容器镜像名称和标签。 
运行上述命令后，可以在http://localhost:8000 上访问该应用程序。


**docker version**
``docker version``

**process**
``sudo docker ps``

**stop app** // xxx 只需要id的前三位数
``sudo docker stop xxx``

## 部署Flask 应用
简单办法：通过脚本生成容器镜像。 创建脚本化容器镜像的命令是``docker build .``。 该命令从一个名为*Dockerfile*的文件读取并执行构建指令（我需要创建这些指令）。 
*Dockerfile*基本上可以认为是一个安装程序脚本，它执行安装步骤来部署应用程序，以及一些容器特定的设置

基本步骤：
- 配置*Dockerfile*
- 写一个*boot.sh* 文件，用来启动Docker容器（写在Dockerfile里面也行）
- ``docker build .`` 命令部署

**Dockfile 例子**
```
FROM python:3.6-alpine

RUN adduser -D microblog

WORKDIR /home/microblog

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY microblog.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP microblog.py

RUN chown -R microblog:microblog ./
USER microblog

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
```

- FROM: 容器的镜像（在此镜像基础上构建）
- RUN: 后面接任意的shell命令(例子中是创建新用户，避免总是使用root)
- WORKDIR: docker中的程序安装目录
- COPY: 从我的电脑中复制一些文件过去（可以用绝对路径，或者相对于WORKDIR的相对路径）（同时run命令后安装requirements.txt中的依赖，并且安装gunicorn以运行web应用）
- ENV: 设置flask app所依赖的环境变量（FLASK_APP）
- EXPOSE: 设置改容器用于服务的端口（这里设置Flask默认的5000）
- ENTRYPOINT: 容器启动时执行的命令([RUN vs CMD vs ENTRYPOINT](https://www.cnblogs.com/CloudMan6/p/6875834.html))

**CMD和ENTRYPOINT的区别：**
https://blog.csdn.net/u010900754/article/details/78526443
- CMD:The main purpose of a CMD is to provide **defaults** for an executing container. These defaults can include an executable, or they can omit the executable, in which case you must specify an ENTRYPOINT instruction as well. (说明这个是在没有entrypoint的情况下默认执行，entrypoint才是真正用来启动container的。cmd的角色定位就是默认，如果你不额外指定，那么就执行cmd的命令，否则呢？只要你指定了，那么就不会执行cmd，也就是cmd会被覆盖。)
- ENTRYPOINT: An ENTRYPOINT allows you to configure a container that will run as an executable.

```
# The CMD instruction has three forms:
 
CMD ["executable","param1","param2"] (exec form, this is the preferred form)
CMD ["param1","param2"] (as default parameters to ENTRYPOINT)
CMD command param1 param2 (shell form)


# ENTRYPOINT has two forms:
 
ENTRYPOINT ["executable", "param1", "param2"] (exec form, preferred)
ENTRYPOINT command param1 param2 (shell form)
```


**boot.sh 例子**

```bash
#!/bin/sh
source venv/bin/activate
flask db upgrade
flask translate compile
exec gunicorn -b :5000 --access-logfile - --error-logfile - microblog:app
```

``exec``让我们的启动进程变成docker的主进程，将与docker有共同的生命周期

``sudo docker build -t microblog:latest .`` // t指定镜像的名称和标签 ``.``是目录

## 第三方应用
容器的存储系统是临时的，所以需要换新的容器的时候数据会丢失。
好的做法是把数据存放在容器之外的位置

### MySQL 容器
类似之前的步骤
- 镜像可以使用官方维护的那个
- 编写Dockerfile, boot.sh文件（其实不用，就用官方的那个 FROM 官方image）
- 启动
- 注意一般情况下需要初始化：root密码，新用户和新用户密码，初始化一个database等等

# Docker Compose
https://www.jianshu.com/p/658911a8cff3
之前只有一个container
当微服务架构的应用系统中包含多个微服务的时候，通过Docker Compose来提高效率

**基本结构**
- project: docker-compose.yml 包含多个服务(比如我的app，redis，mysql)
	- redis，mysql不用我build因为别人build好了我可以直接下
- service: 包含多个containers
- container

**安装**
略

**组件**
- Dockerfile
- docker-compose.ymal
- ``docker compose up``

可以先build web app，然后在yaml里面指定image来pull。
也可以不build，在yaml里面build

## docker-compose 命令
```bash
docker-compose up
docker-compose down
```
## docker-compose.yml 配置
好难啊不会

# 其他
Docker-compose 部署Flask+celery+MySQL+redis （使用docker compose 相对复杂，但还没用到swarm等）
docker镜像减小一次经历
