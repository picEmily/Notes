## 安装
从windows store安装
在windows里面打开linux的服务(baidu)
现在已经可以用了

## 连接
- 直接点开：出来的就是terminal;或者在cmd里面用bash命令
- 远程桌面
- x server

### 远程桌面
ref: https://www.interserver.net/tips/kb/install-xrdp-ubuntu-server-xfce-template/

```bash
## sudo

apt-get update
apt-get install xrdp
apt-get install xfce4
## 或者（有个blueman组件安装不成功，手动remove就好了）
## 装这个xubuntu就不需要自己装python，firefox了
sudo apt-get install xubuntu-desktop
echo "xfce4-session" > ~/.xsession
/etc/init.d/xrdp start
/etc/init.d/xrdp status
```
然后再terminal里面
``ifconfig`` 得到ip地址（我找的是wlan那个地址）

在windows里面自带的远程桌面中(3389是默认端口)：
ip:3389
或者127.0.0.1:3389
username: [linux username]
进入了以后选xrong,用设置的linux密码登录

### xserver 登录
- 选择xserver：有很多，我下载的是：https://kb.lsa.umich.edu/lsait/index.php/X_Servers_for_Windows
- 启动ssh

```bash
## WSL自带 openssh, 需要手动启动：
sudo service ssh start

## 自带的SSH存在一点问题，需要重新生成Key，然后重启服务:
sudo ssh-keygen -A 
sudo service ssh --full-restart

## 编辑配置：
## 将找到PasswordAuthentication项并改为 yes，允许用户名+密码登陆
sudo vi /etc/ssh/sshd_config
```
## 各种配置
### root 
sudo su -

### 换源
ubuntu18.04更换国内源

- 1.备份原始源文件source.list
``sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak``
- 2.修改源文件source.list
（1）终端执行命令：``sudo chmod +777 /etc/apt/sources.list``更改文件权限使其可编辑；
（2）执行命令：``sudo vim /etc/apt/sources.list``打开文件进行编辑；
（3）删除原来的文件内容，复制下面的任意一个到其中并保存（常用的是阿里源和清华源，推荐阿里源，内容可以去博客复制）；
阿里源：
```
deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
```
清华源：
```
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-proposed main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-proposed main restricted universe multiverse
``` 
163源：
```
deb http://mirrors.163.com/ubuntu/ bionic main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ bionic-security main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ bionic-updates main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ bionic-backports main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ bionic main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ bionic-security main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ bionic-updates main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ bionic-backports main restricted universe multiverse
```

- 3.更新源
更新软件列表，换源完成。
``sudo apt-get update``
``sudo apt-get upgrade``

### 安装中文utf8

### 清理
```
sudo apt --fix-broken install

sudo apt-get autoremove
sudo apt-get autoclean
```


### 安装浏览器
- firefox

```bash
sudo apt-get install firefox
## firefox中文问题
sudo apt-get install firefox-locale-zh-hans(不知道有没有用)
```
- 安装chromimum(失败)

```
sudo apt --fix-broken install
sudo apt-get install chromium-browser
sudo apt-get remove chromium-browser
```

### 安装vscode(失败)
通过官方PPA安装Ubuntu make
```
sudo add-apt-repository ppa:ubuntu-desktop/ubuntu-make
sudo apt-get update
sudo apt-get install ubuntu-make
```
通过umake命令安装VSCode ``umake ide visual-studio-code``之后会确认安装路径，直接回车就可以；再会确认安装，输入a。
``umake ide -r visual-studio-code``卸载

### mysql
https://www.cnblogs.com/shouhuqingtian/p/8409719.html
```
## 如果之前安装错误，清空安装文件
sudo apt-get purge mysql* && sudo apt-get autoremove && sudo rm -rf /etc/mysql

## 查看可安装版本
apt-cache show mysql-server

## 安装和启动
sudo apt-get install mysql-server
sudo service mysql start
sudo service mysql restart
sudo mysql -u root -p
```

错误解决：
MySQL 5.7 No directory, logging in with HOME=/
```
sudo service mysql stop
sudo usermod -d /var/lib/mysql/ mysql
sudo service mysql start
```
## 远程开发
https://zhuanlan.zhihu.com/p/49227132
Pycharm 配置远程Python环境

wsl的路径
``\\wsl$``

https://www.cnblogs.com/lepeCoder/p/wsl_dir.html