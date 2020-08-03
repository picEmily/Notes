# Linux Command Notes
## Intro to shell
- do everything in shell  
- interactive: execute command
- customizable 
- powerful: doing anything

how to make shell as easy as possible 
- C shell: 
- bash(popular) - z shell 

commands 
- ls
- cd
- man [command]

relative and absolute path
- ~ means home
- / root start at the very root
- .. one div up
- . curr folder

z shell

- customize tab completion

up down to access previous commands

how to get out 
- contorl + c; control + D(close the shell)
- control + z : minimize(jobs, bg)_

### WHy should we use linux
fast

### how to install Linux 
- in harddrive
- virtual machine(much more useful in this situation)
	- on top on windows, can have dual boot 
intallation process
- VM software: VMware
- Linux image: Ubuntu
	- popular
	- a large amount of software
	- terminal 

## Pipe I/O
### Pipe
input from an standard output
- ``|`` means pipe
- ``cat``命令是linux下的一个文本输出命令，通常是用于观看某个文件的内容的；cat主要有三大功能：
	1. 一次显示整个文件。
	$ cat   filename
	2. 从键盘创建一个文件。
	$ cat  >  filename
	只能创建新文件,不能编辑已有文件.
	3. 将几个文件合并为一个文件。
	$cat   file1   file2  > file

> 补充：
> - ``diff file1 file2`` 比较file1 file2 内容
> - ``man [command]``: see the manual of this command
> - ``grep`` 常用在regex中

``grep cat test.txt | grep bird``: 
It's a kind of pipe: from test.txt, grep the sentence containing cat, from the result, grep the sentence containing bird

### output to file
``>`` means **rewrites** to a file
``>>`` means **append** to a file

``cat txt1 > foo`` check it by `` diff txt1 foo`` // we can't do it if file exists
``grep bird txt1 > foo`` 

#### 练习

- output bash error to temp file  
``safdsfasf 2> temp`` 2 means err, bash will say command not found. This scrips will be output in a new file called temp

- List the contents of your home directory and store that in a file  
``ls 1>temp``

- List the contents of your home directory and append it to the same file ``ls 1>>temp``

- Thought question: what happens if you have a file called foo and you run cat < foo > foo? 
Intuitively, that would say to use foo as the input to cat and output that to foo. Why isn't that the case? 
Hint: Try running something that doesn't create any output, for instance: touch bar > foo. Why is foo empty even though the command never tried to write to it? Note that CSH on the Stanford machines has 'noclobber' option set. This will prevent you from overwriting any files ("clobbering" them). That is annoying and will prevent you from doing this exercise. Instead, use ZSH.  
[https://www.unix.com/unix-for-dummies-questions-and-answers/541-overwrite.html](https://www.unix.com/unix-for-dummies-questions-and-answers/541-overwrite.html)
- Thought question: what happens if you have a file called foo and you run cat < foo >> foo? 
Intuitively, that would print out foo and append it to foo, basically doubling the file. Why isn't that the case? 
Hint: How big is the file at the start and then how big is the file after cat has gone through the first line? Note: ctrl+C is your friend.  
``cat < temp >> temp``  
 temp: cannot overwrite existing file

### Input from file 
>``chmod u+x [filename]`` 给文件增加执行权限[参考](https://www.cnblogs.com/adolfmc/p/5898115.html)

1. ``cat nums-0-999 | python read-input.py`` 把*nums-0-999* 的内容作为*read-input.py*的输入（执行过增加执行权限的命令以后可以``cat nums-0-999 | ./read-input.py``）
2. ``./read-input.py < nums-0-999`` 第二种方法，意思一样

#### Tee
what is happening when piping? 

``ping google.org | tee ping``

### head, tail
- Print the last three lines of table
	- ``tail -n 100 table`` // 显示最后100行数据
	- ``tail -n -100 table`` //显示100到末尾行
- Print the first three lines of table
	- ``head -n 5 table `` // 显示前n行
	- ``head -n -5 table`` // 显示除了最后n行的内容
- Print only the second and third lines of table
	- ``head -2 table | head -3``// 其实sed更方便
- 显示5~10行
	- ``sed -n '5,10p' filename``
	- ``sed -n '5,10p' filename`` // 只显示第10行

#### sort
``tail -n +3 pumpkinsizes | sort -n -k 2 -t '|'``
``cat words-sorted | uniq  > words-uniq``
``cat words-sorted | uniq -c -d > words-count``
``cat words | tr ' ' '\n' | sort > words-sorted2``

#### Diff
找不同
``diff file1-from file2-to`` 
``diff dir1 dir2``

**flags in diff**
-b -B 
``diff file1 file2 -B``
 ignore whitespace within line/ between line 
 ``diff -y file1 file2`` side by side显示 ``，通过--width=``来调整
 
#### Find
search file
 
 // find by name pattern 
 ``find . -name "*resume*"`` == ``find -name "*resume*"`` // current dir by default
 
 // find by permisions
 ``find . -perm a=rwx,g=twx,u=rwx`` 

// find ?? 
``name "*resume*" -exec echo {} \;``

// locate search in entire system
``sudo update db``
``locate "*resume*"``
``locate "**resume" | grep xxx``

## RegExp 
grep **pattern** file
- ``grep include tcp.c``
- ``grep "hello world" tcp.c`` 或者 ``grep hello \  world tcp.c``

#### ``.`` means every char
``grep s.ack tcp.c`` // . 指的是任何字母 == ``grep s[mn]ack tcp.c`` smack / snack

#### ``*`` repeat more than zero 
``N.*`` means Null, Nu，Not... 等等
// find an US address
// start with one or more number + some char follow by space + two char capital state name + num repeated 5 times 
``grep "[0-9]* .* [A-Z][A-Z] [0-9]{9} tcp.c``

#### ``^`` 除了
``grep "[^0-9]{5}"`` // everything except for 0~9

#### ``{}``
``hello{5}`` means hellooooo
``(hello){5}`` means hello 5次

#### ``$ ^``
// start and end line char
``$`` means end with $
``^int`` means start with int
// **no number** in a line
``^[^0-9]*$`` // the entire in the middle has to be one or more char that is not number
``([^ ]*)`` // means one word

#### ``()`` group
``(xxx)`` means group ``(?:xxx)`` means ignore group 

#### find and replace 
```python3
python
import re
re.sub()
```



> ``echo``在显示器上显示一段文字，一般起到一个提示的作用。
> ``echo cs1u*`` print all dir in the curr dir that begin with cs1u

#### homework
因为我没有
在``~/.zshrc or ~/.bashrc file:`` 配置``alias grep="grep -P"``，我需要一直用转义字符(escape char)

1. // 只选择123-456-7890有dash的数字
``grep "[0-9]\{3\}\-[0-9]\{3\}\-[0-9]\{4\}" golded cs1u*``
// -o 表示只显示匹配，不然会把一行都打印出来
// -r 表示逐层遍历目录寻找

2. // 有dash和没有dash的都要
``grep "[0-9]\{3\}[\-]*[0-9]\{3\}[\-]*[0-9]\{4\}" cs1u* golden > output1``
// 做法就是``[\-]*``这样以来可以有0个或者以上个dash

3. // 有括号的也要
``grep "[\(]*[0-9]\{3\}[\)]*[\-]*[0-9]\{3\}[\-]*[0-9]\{4\}" cs1u* golden > output1``

4. // 可能有不配对的括号，保证要配对，用到OR

``grep "[0-9]\{3\}\-[0-9]\{3\}\-[0-9]\{4\}\|\([0-9]\{3\}\)[0-9]\{3\}\-[0-9]\{4\}\|[0-9]\{3\}[0-9]\{3\}[0-9]\{4\}" cs1u* golden > output1``
不能handle malformed

## Python Shell Script
### use Python in shell/ use shell in python
- how to run shell in python 
- search for ``pyhon shell command`` to see how to run python in shell

#### run shell in python
**using python os**

```python
python
>> import os
>> os.system('ls') # the same as typing ls in terminal
```
#### run Python in shell
In the python file, argv[] is past to it. Note that sys.argv[0] is the name of file, sys.argv[1] 才是传进去的argv1
``python test.py argv1 argv2``

How would you access command-line arguments from a python script?
``sys.argv`` get the argument from the terminal

### Permissions

if we create a new python file and want to execute it, we need to give it executable permission``chmod u+x xxx.py``. Then we can execute with ``./xxx.py``. Or just using ``python xxx.py`` without changing permission. 
#### change permission of files
``ls -l`` tells:
- permissions: d(dir), -(normal file), rwx(read, write, execute), order(owner, group, global)
- owner
- group
- size
- date
- name
- color: green(executable), blue(a directory),black(regular), pink()

1. ``chmod [ugo][+-][0-7]`` // 添加/删除权限
2. 直接设置权限	
using the sum of 4 or 2 or 1 in the command
r == 4 w == 2 x == 1
adding the permission I want 
u:user g:group o:global

进制: 8进制 octal / decimal 看情况

e.g.
``chmod 720 directory_name`` // means user can rwx, group can only write, global can do nothing

#### ``subprocess.Popen()`` and ``os.system()`` 区别
[https://stackoverflow.com/questions/4813238/difference-between-subprocess-popen-and-os-system](https://stackoverflow.com/questions/4813238/difference-between-subprocess-popen-and-os-system)

# Network

``scp [file1] [file2]`` // don't have to be the local computer
``user@host:file_path``

``wget`` // download
``wget [the place you want to download]``

## cURL (不读cURL，读可额儿)
参考[https://blog.csdn.net/chenliaoyuanjv/article/details/79689028](https://blog.csdn.net/chenliaoyuanjv/article/details/79689028)
``cURL`` // client for urls
``curl http://google.com:80``
``curl --location`` // redirect to the new location
``curl -o google.com`` // do the same thing as ``wget``
``curl --libcurl foo.c google.com`` // access everything you can use in curl in c library

how webapp works
GET: everything in the url
``www.google.cim/search?q=stanford+"openclassroom"&foo=bar`` // 参数都在url里面
not all info is in the url->the same url with different info
POST:

get request in curl:
``curl "google.com"``

post request in curl:
``curl google.com -d [xxx]`` // post data
``curl google.com -F picures@.xxx`` // post form
如果有特殊字符
``--data-urlencode "xxx"``

``-I`` show only the headers 
``-i`` show the page as a whole
``-v`` verbose: port, ip, the request, the user agent(e.g. firefox)
get rid of content-length
``-v -H "content-length:"``
``-x PUT`` // 指定verb
``-A mozilla/4.05`` // 指定agent

1. ``https://stanford.edu/~jainr/cgi-bin/simple_vote_action.php?candidate=2``
2. ``curl -d "candidate=2" https://stanford.edu/~jainr/cgi-bin/secure_vote_action.php`` // ``curl https://stanford.edu/~jainr/cgi-bin/secure_vote_action.php -d "candidate=2"``

#### 將cookie存檔
curl -c ~/cookie.txt http://stanford.edu/~jainr/cgi-bin/presidential.php
#### 載入cookie到request中 
(都不对呀)
curl -b ~/cookie.txt http://stanford.edu/~jainr/cgi-bin/super_secure_vote.php

4. [https://stackoverflow.com/questions/32330737/ubuntu-using-curl-to-download-an-image](https://stackoverflow.com/questions/32330737/ubuntu-using-curl-to-download-an-image)
	- ``curl https://stanford.edu/~jainr/cgi-bin/curl-meme.jpg > ~/image.jpe``
	- ``wget https://stanford.edu/~jainr/cgi-bin/curl-meme.jpg`` // 有错Disabling SSL due to encountered errors.
	- ``curl -O https://stanford.edu/~jainr/cgi-bin/curl-meme.jpg`` // 本质同上一句 但是上一句不能运行（可能是我没有wget）

答案：
in one line
``curl http://stanford.edu/~jainr/cgi-bin/super_secure_vote_action.php -d candidate=1000 --cookie president=has_visited``

use cookie directly in this way:
``curl http://stanford.edu/~jainr/cgi-bin/super_secure_vote.php --cookie president=has_visited``



定时关机：
https://askubuntu.com/questions/505929/shutdown-after-a-certain-time

定时运行文件：
```
# Launch script in background
./my_script.sh &
# Get its PID
PID=$!
# Wait for 2 seconds
sleep 2
# Kill it
kill $PID
```