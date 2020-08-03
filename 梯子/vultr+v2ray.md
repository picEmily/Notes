购买服务器
silicon valley 
10$
ubuntu 16

ping一下看看通不通
ssh 进去

一键脚本（不知道哪个更好）
``
bash <(curl -L -s https://install.direct/go.sh)
``

``
bash <(curl -s -L https://git.io/v2ray.sh)
``

记住
```
PORT:25705
UUID:b3dbf204-1165-4df6-8060-a372cd433725
```
或者
```
vi /etc/v2ray/config.json
```

```
systemctl start v2ray
systemctl enable v2ray
```

升级内核装bbr
```
apt update
apt install --install-recommends linux-generic-hwe-16.04
uname -a
```

修改 ``/etc/sysctl.conf``


本文介绍在Ubuntu 16.04系统中开启TCP BBR以提升网络性能，实现更高的带宽和更低的延迟。你可以在Linux桌面上启用TCP BBR，以改善整体Web浏览体验，如果有Linux Web服务器，TCP BBR可以为你的网站访问者实现更快的网页下载。可先参考Ubuntu 18.04快速开启Google BBR一文。

 

在Linux上检查TCP拥塞控制算法

默认情况下，Linux使用Reno和CUBIC拥塞控制算法，要检查可用的拥塞控制算法，请运行以下命令：

sysctl net.ipv4.tcp_available_congestion_control

输出如下：

net.ipv4.tcp_available_congestion_control = cubic reno

要检查当前使用的拥塞控制算法，请运行：

sysctl net.ipv4.tcp_congestion_control

输出如下：

net.ipv4.tcp_congestion_control = cubic

 

安装Linux 4.9内核或更高版本

自内核版本4.9以来，Linux支持TCP BBR，使用以下命令检查Linux内核版本：

uname -r

在Ubuntu 16.04桌面上，内核版本是4.10：

4.10.0-40-generic

升级内核参考：使用Ukuu在Ubuntu/Linux Mint上安装Linux Kernel 5.0的方法。

其实在Ubuntu 16.04上安装Linux新内非常容易，不必从Ubuntu网站手动下载内核，只需安装硬件启用Stack（HWE），它为Ubuntu LTS版本提供了更新的内核：

sudo apt update

sudo apt install --install-recommends linux-generic-hwe-16.04

 

在Ubuntu 16.04中启用TCP BBR

确认使用内核4.9或更高版本后，编辑sysctl.conf文件：

sudo nano /etc/sysctl.conf

在文件末尾添加以下两行：

net.core.default_qdisc=fq

net.ipv4.tcp_congestion_control=bbr

保存并关闭文件，然后重新加载sysctl配置：

sudo sysctl -p

现在检查使用中的拥塞控制算法：

sysctl net.ipv4.tcp_congestion_control

输出如下：

net.ipv4.tcp_congestion_control = bbr

至此，你已经在Ubuntu系统上成功启用TCP BBR了。