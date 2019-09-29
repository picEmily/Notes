# crontab命令讲解
man cron（cron是服务，利用crontab来编辑）
```
NAME
       cron - daemon to execute scheduled commands (Vixie Cron)

SYNOPSIS
       cron [-f] [-l] [-L loglevel]

DESCRIPTION
       cron is started automatically from /etc/init.d on entering multi-user runlevels.

OPTIONS
       -f      Stay in foreground mode, don't daemonize.

       -l      Enable  LSB  compliant names for /etc/cron.d files. This setting, however, does not affect the parsing
               of files under /etc/cron.hourly, /etc/cron.daily, /etc/cron.weekly or /etc/cron.monthly.

       -n      Include the FQDN in the subject when sending mails. By default, cron will abbreviate the hostname.

       -L loglevel
               Tell cron what to log about jobs (errors are logged regardless of this value) as the sum of  the  fol‐
               lowing values:

                   1      will log the start of all cron jobs

                   2      will log the end of all cron jobs

                   4      will log all failed jobs (exit status != 0)

                   8      will log the process number of all cron jobs

               The  default  is  to  log the start of all jobs (1). Logging will be disabled if levels is set to zero
               (0). A value of fifteen (15) will select all options.

```

man crontab
```
CRONTAB(1)                                     General Commands Manual                                     CRONTAB(1)

NAME
       crontab - maintain crontab files for individual users (Vixie Cron)

SYNOPSIS
       crontab [ -u user ] file
       crontab [ -u user ] [ -i ] { -e | -l | -r }

DESCRIPTION
       crontab is the program used to install, deinstall or list the tables used to drive the cron(8) daemon in Vixie
       Cron.  Each user can have their own crontab, and though these are files in /var/spool/cron/crontabs, they  are
       not intended to be edited directly.

       If the /etc/cron.allow file exists, then you must be listed (one user per line) therein in order to be allowed
       to use this command.  If the /etc/cron.allow file does not exist but the /etc/cron.deny file does exist,  then
       you must not be listed in the /etc/cron.deny file in order to use this command.

       If  neither  of  these files exists, then depending on site-dependent configuration parameters, only the super
       user will be allowed to use this command, or all users will be able to use this command.

       If both files exist then /etc/cron.allow takes precedence. Which means that /etc/cron.deny is  not  considered
       and your user must be listed in /etc/cron.allow in order to be able to use the crontab.

       Regardless  of  the existance of any of these files, the root administrative user is always allowed to setup a
       crontab.  For standard Debian systems, all users may use this command.

       If the -u option is given, it specifies the name of the user whose crontab is to be  used  (when  listing)  or
       modified  (when  editing).  If this option is not given, crontab examines "your" crontab, i.e., the crontab of
       the person executing the command.  Note that su(8) can confuse crontab and that if you are running  inside  of
       su(8) you should always use the -u option for safety's sake.

       The  first form of this command is used to install a new crontab from some named file or standard input if the
       pseudo-filename ``-'' is given.

       The -l option causes the current crontab to be displayed on standard output. See the note  under  DEBIAN  SPE‐
       CIFIC below.

       The -r option causes the current crontab to be removed.

       The  -e option is used to edit the current crontab using the editor specified by the VISUAL or EDITOR environ‐
       ment variables.  After you exit from the editor, the modified crontab will be installed automatically. If nei‐
       ther of the environment variables is defined, then the default editor /usr/bin/editor is used.

       The  -i  option  modifies  the  -r option to prompt the user for a 'y/Y' response before actually removing the
       crontab.

```

```
# 编辑定时任务
crontab -e
# 查看定时任务
crontab -l
# 删除定时任务
crontab -r
```
- -u user：用来设定某个用户的crontab服务；
- file：file是命令文件的名字,表示将file做为crontab的任务列表文件并载入crontab。如果在命令行中没有指定这个文件，crontab命令将接受标准输入（键盘）上键入的命令，并将它们载入crontab。
- -e：编辑某个用户的crontab文件内容。如果不指定用户，则表示编辑当前用户的crontab文件。
- -l：显示某个用户的crontab文件内容，如果不指定用户，则表示显示当前用户的crontab文件内容。
- -r：从/var/spool/cron目录中删除某个用户的crontab文件，如果不指定用户，则默认删除当前用户的crontab文件。
- -i：在删除用户的crontab文件时给确认提示

# 流程讲解
https://blog.csdn.net/xiyuan1999/article/details/8160998
https://blog.csdn.net/errors_in_life/article/details/72778816
https://www.cnblogs.com/ftl1012/p/crontab.html
https://blog.csdn.net/fdipzone/article/details/51778543
https://blog.csdn.net/putin1223/article/details/46727283

## 编辑crontab文件
``crontab -e``进入编辑
规则参考：https://blog.csdn.net/xinyflove/article/details/83178876
在线生成：http://cron.qqe2.com/
https://tool.lu/crontab/
http://www.matools.com/crontab

**时间格式**
分 时 日 月 星期 要运行的命令

- 第1列分钟0～59
- 第2列小时0～23（0表示子夜）
- 第3列日1～31
- 第4列月1～12
- 第5列星期0～7（0和7表示星期天）
- 第6列要运行的命令

## 开始执行文件
启动服务需要sudo
```
sudo service cron start
sudo service cron stop
sudo service cron restart
sudo service cron status
```

## 输出
https://blog.csdn.net/DN_XIAOXIAO/article/details/78322906
https://blog.csdn.net/Solmyr_biti/article/details/50683279
https://blog.csdn.net/u012129607/article/details/80418149

常用
``* * * * * ~/Desktop/test_cron.sh >> ~/Desktop/test_cron.log 2>&1``
正常print和错误日志在一起被输出

``&>/dev/null 2>&1``不输出日志


# 注意
设置环境变量
crontab本身没有环境变量，加入要执行python文件。需要在crobtab里面写 ``/PATH/python xxx.py``，所以用sh文件来运行会更方便 

跟用户有关，不要乱sudo
ps查看状态
log是>>

记得给被执行的文件都加上可执行权限

执行shell报错source:notfound
用bash来执行文件，因为sh里面没有source，不能开虚拟环境

crontab的默认执行路径为：当前用户的根路径。

# 在Docker中运行cron服务
crontab里面root不能丢（需要指定用户，平时不需要，放在/etc/cron.d/文件夹下需要，不然就要）
（实测：不加的话，我手动可以启动，但是dockerfile里面cmd命令不能启动）

https://www.jianshu.com/p/351a2b2b416b
https://stackoverflow.com/questions/37458287/how-to-run-a-cron-job-inside-a-docker-container
https://www.awaimai.com/2615.html

use host network config
https://docs.docker.com/network/host/

docker cron backup mysql


https://medium.com/@jonbaldie/how-to-run-cron-jobs-inside-docker-containers-26964315b582