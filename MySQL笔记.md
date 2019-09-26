# Mysql 学习笔记
## 下载
### 下载
https://www.cnblogs.com/reyinever/p/8551977.html
官网下载 MySQLcommunity sever
解压缩
### 配置环境变量
变量名：MYSQL_HOME
变量值：E:\mysql-5.7.20-winx64
path里添加：%MYSQL_HOME%\bin;
## 简单启动
开启binary log
```
# 由于我实在找不着my.cnf 或者my.ini文件
# 所以我在安装mysql的目录下自己建立了一个
# ./my.cnf
[mysqld]
log-bin=mysql-bin
server-id=1
```

第一次使用mysql
```
mysqld --initialize-insecure --user=mysql ## 要带user参数创建用户
mysqld --install ## mysqld --remove
net start mysql ## net start mysql
```
## 注册用户
### 生成data
以管理员身份运行cmd
进入E:\mysql-5.7.20-winx64\bin 下
执行命令：``mysqld --initialize-insecure --user=mysql``  
在E:\mysql-5.7.20-winx64目录下生成data目录
### 启动服务
执行命令：``net start mysql``  启动mysql服务，
若提示：服务名无效  解决办法：mysqld -install
### 登陆
登录mysql:(因为之前没设置密码，所以密码为空，不用输入密码，直接回车即可）

E:\mysql-5.7.20-winx64\bin>``mysql -u root -p``
Enter password: 回车符
### 修改root密码，注册新用户
CREATE USER 'wzq'@'localhost' IDENTIFIED BY '123456';
GRANT ALL ON *.* TO 'wzq'@'localhost';

## 创建数据库
https://www.runoob.com/mysql/mysql-tutorial.html
在mysql terminal中
``mysql> create DATABASE appdb;``
``mysql> use appdb;``

**问题**
我之前的命令在我自己的电脑上是好的，docker里面不知道为啥有点问题，用这里的命令就好了
```
create DATABASE WEBSERVICE character set utf8;
CREATE USER 'wzq'@'%' IDENTIFIED BY '123456';
GRANT ALL privileges on WEBSERVICE.* to 'wzq'@'%';
```

## 创建table
例子
```mysql
root@host# mysql -u root -p
Enter password:*******
mysql> use RUNOOB;
Database changed
mysql> CREATE TABLE runoob_tbl(
   -> runoob_id INT NOT NULL AUTO_INCREMENT,
   -> runoob_title VARCHAR(100) NOT NULL,
   -> runoob_author VARCHAR(40) NOT NULL,
   -> submission_date DATE,
   -> PRIMARY KEY ( runoob_id )
   -> )ENGINE=InnoDB DEFAULT CHARSET=utf8;
Query OK, 0 rows affected (0.16 sec)
mysql>
```
## 数据库操作
### insert
```mysql
mysql> INSERT INTO runoob_tbl 
    -> (runoob_title, runoob_author, submission_date)
    -> VALUES
    -> ("学习 PHP", "菜鸟教程", NOW());
Query OK, 1 rows affected, 1 warnings (0.01 sec)
```
### Query
要看user的话再database:mysql table:user里面
query略

## 查看数据库信息
``SHOW DATABASES;``
``SHOW TABLES;``

# Flask + MySQL
这里我用root登陆，格式是[root]:[password]\(我的密码是空)。MySQL端口默认3306，然后用我创建的appdb。
注意sqlite可以直接用python来建数据库，table。但是MySql要先在外面建好db和table。


```python3
# settings.py
# app path
base_dir = os.path.abspath(os.path.dirname(__file__))  # 返回绝对路径
# sqlalchemy 配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/appdb'  # MySql
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'app.db')  # Sqlite
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
```
```python3
# app.py 
# 导入配置
app.config.from_object(config.get('default'))
```
```python3
# models/user.py
class User(UserMixin, db.Model):
    """define a user

    Attributes:
        id: define the id of a user
        username: define username of a user
        password: define password of a user
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)

    def check_password(self, password):
        return password == self.password

    def __repr__(self):
        return '<User %r>' % self.username
```
```python3
# routes/user.py
通过python添加用户
@app.route('/')
def register():
	user = User(username=form.username.data, password=form.password.data)
	db.session.add(user)
	db.session.commit()
```

# Cheat sheet
```bash
## ubuntu 18 lts

INSERT INTO runoob_tbl??? 

## 看mysql启动没
ps -ef | grep mysqld

## 安装：
sudo apt-get install mysql-server
sudo apt-get isntall mysql-client
sudo apt-get install libmysqlclient-dev

## 创建用户
CREATE USER 'wzq'@'localhost' IDENTIFIED BY '123456';
GRANT ALL ON *.* TO 'wzq'@'localhost';

## 登录：
sudo mysql -u root -p 

create DATABASE WEBSERVICE;
use WEBSERVICE;

show databases;
show tables;

## 注意：mysql db，table名字区分大小写,命令不区分
## flask里面连接的名字是小写？？（我不知道在哪连接的）

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

DROP TABLE USERS

INSERT INTO user
(username, password)
VALUES
("admin", "admin");

quit
```

## 可视化工具
navicat 
- 可以快速地看到表的内容
- 运行sql语句
- 改data，改表的结构，设置字段（key,变量类型等等）
- 不会写的sql代码可以用navicat点点点自动生成

## python操作mysql
python2
https://www.runoob.com/python/python-mysql.html

python3
``pip3 install pymysql``
https://www.runoob.com/python3/python3-mysql.html

# FAQ
### RuntimeError: cryptography is required for sha256_password or caching_sha2_password
装8会有这个问题
装5.7

### 查看数据类型
https://jingyan.baidu.com/article/495ba841e2db3638b30ede2c.html

### 几种数据类型 
LONTTEXT数据类型不需要括号和长度
记得db.commit() 否则不会改写

DATETIME 有好几种相似的

## SQL补充
### insert
``INSERT INTO table_name (列1, 列2,...) VALUES (值1, 值2,....)``

类似的还有``SELECT INTO``
从一个表选取数据插入另一个表
- 用``INSERT INTO``: ``INSERT INTO [new_tablename] (SELECT * FROM [ole_tablename] WHERE ID<100)``
- 用``SELECT INTO``: ``SELECT *
INTO new_table_name [IN 'external_database_name'] 
FROM old_tablename``

### keys
如何指定primary key 和foreign key 并使用
http://www.w3school.com.cn/sql/sql_primarykey.asp
- 创建时指定primary key, constraint primary key
- 对已存在的列设置primary key（该列必须为not null）
- 撤销primary key约束
- 如何给table增加主键列并让其自增？？？（我之前用navicat点点点实现）

http://www.w3school.com.cn/sql/sql_foreignkey.asp
指定reference，其他差不多

### index
用来更快的查找，用户无法看到
仅在需要的列上创建
```sql
CREATE (UNIQUE) INDEX index_name
ON table_name (column_name_1, column_name_2)
```

### SQL 内建函数
常用的AVG(), COUNT()这些
合计函数常常需要搭配``GROUP BY``, ``HAVING``

# 数据恢复
打开binary logs

```
# 常用命令
show binary logs;
show variables like '%log_bin%'

# 可以看到每一步干了啥，找到错误的position
show binlog events in 'mysql-bin.000001';  

# mysqlbinlog 输出可执行文件 把需要用的导出来
mysqlbinlog .\data\mysql-bin.00000 --stop-position 2028 > data.sql

# mysql 客户端中
mysql>source data.sql 

```
https://www.iteblog.com/mysql-binlog_basic_usage/
https://learnku.com/articles/20628#2a302f
https://blog.csdn.net/chaigang/article/details/82350399

坑：不要用powershell

# 基础笔记

- 并发控制
	- 读写锁
	- 锁粒度
- 事务
	- 事务的隔离级别
- 多版本并发控制MVCC

## MVCC
用于**事务型**存储引擎，存储引擎实现的不是简单的行级锁，可以将MVCC理解为行级锁的变种，但是会减少很多加锁的操作。
具体的实现方式是在每行后保存额外的两列：行的创建时间，行的过期时间（时间指的不是具体时间，而是引擎里记录的每个事务的版本号，每个新的事务都会递增版本号）
仅仅可用于**REPEATABLE READ**和**SERIALIZABLE**的隔离级别
关键词： 某个时间点的**快照** 乐观并发控 悲观并发控制


- SELECT: 只查找版本号更早的行，行的删除版本未定义或更晚 
- INSERT: 保存创建版本号为当前版本号
- DELETE: 保存删除版本号为当前版本号
- UPDATE: 等同于INSERT+DELETE操作

## 事务的隔离级别
隔离级别高，不容易出错，但是并发能力会小，开销会高。
- READ UNCOMMITED：很少使用，有脏读问题
- READ COMMITTED：（又叫不可重复读）
- REPEATABLE READ：MySql默认隔离级别，没有脏读问题，同一个事务中每次读操作结果一样。有幻读问题。
- SERIALIZABLE：确保数据的一致性且可以接受没有并发。

