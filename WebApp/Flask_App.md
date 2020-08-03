# Flask 学习笔记
## 基本使用
### 最简单的app
- 官方文档
- 动物书作者的github: 
https://github.com/miguelgrinberg/flasky-with-celery
https://github.com/miguelgrinberg/flask-celery-example

### 乱七八糟的点

**启动**
```
$ export FLASK_APP=hello.py
$ flask run
 * Running on http://127.0.0.1:5000/
```
webbrower: http://127.0.0.1:5000/     启动
``export FLASK_ENV=development`` // 调试模式

**route 设置链接地址**
``@app.route('/hello')`` // route  

**url_for**
``url_for`` dynamic generate url 
``url_for()`` 函数用于构建指定函数的 URL。它把函数名称作为第一个 参数。它可以接受任意个关键字参数，每个关键字参数对应 URL 中的变量。未知变量 将添加到 URL 中作为查询参数。

``test_requests_context()`` 用来测试，在with 中使用

/test/    可以自动重定向
/test     保证url唯一，不能自动重定向


**blueprint**
BluePrint 用来模块化
分路由中由``form_test = Blueprint('form_test', __name__)``创建蓝图，
而后在主路由中通过app.register_blueprint(form_test)注入
注册app.register_blueprint(login_page)

**Flask_login**
@login_required 需要登陆才能访问


@@login_manager.user_loader
You will need to provide a user_loader callback. This callback is used to reload the user object from the user ID stored in the session. It should take the unicode ID of a user, and return the corresponding user object.
```python3
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
```

user_loader坑 类似的原因
flask报错：flask.cli.NoAppException: Could not import app
https://blog.csdn.net/yangwenwu11514/article/details/88364887

步骤：
in app.views.__init__
创建app
declare login manager
user_loader

**models**
models里面只放定义好的user的模型

之后可以再把in app.views.__init__里的再封装到extension.py里面


For the common case of having one Flask application all you have to do is to create your Flask application, load the configuration of choice and then create the SQLAlchemy object by passing it the application.
Once created, that object then contains all the functions and helpers from both sqlalchemy and sqlalchemy.orm. Furthermore it provides a class called Model that is a declarative base which can be used to declare models:
create db:
To create the initial database, just import the db object from an interactive Python shell and run theSQLAlchemy.create_all() method to create the tables and database:

**config**
Config可以都写道config.py 里面
随便打开一个模板照着写就好


**Jinja2 模板系统还支持流程控制语句  **
wtf 表单https://www.cnblogs.com/liyang93/p/7218764.html
if form.validate_on_submit():
1. 不能为空，
2. 在form中添加validator，否则总是返回false
3. 先暂时关闭CSRF

### config
### 调试
### 项目常用结构
flask开发组成员：https://www.jianshu.com/p/49dc66141d20
动物书作者：
https://blog.miguelgrinberg.com/post/using-celery-with-flask
https://blog.miguelgrinberg.com/post/celery-and-the-flask-application-factory-pattern

# Flask app 项目
- 注册登录系统(mysql实现存储)
- 异步extentions(celery+redis)
- 前端页面

## 工具

sqlalchemy 数据库功能
Flask-WTF 做表单验证
Flask_login 做登录功能

## 思路
web server框架： 有哪几个函数和功能
Blueprint：分成哪几个模块

## 实现注册登录

## celery + reddis实现异步
https://cloud.tencent.com/developer/news/334913

异步任务async task是什么
https://www.runoob.com/w3cnote/android-tutorial-ansynctask.html
答: 
同步：当我们执行某个功能时，在没有得到结果之前，这个调用就不能返回！
简单点就是说必须等前一件事做完才能做下一件事
异步：和同步则是相对的，当我们执行某个功能后，我们并不需要立即得到结果，我们可以正常地做其他操作，
这个功能可以在完成后通知或者回调来告诉我们；
还是上面那个后台下载的例子，后台下载， 我们执行下载功能后，我们就无需去关心它的下载过程，
当下载完毕后通知我们就可以了~

Flask sent task to Redis, Celery accept task from Redis
Celery sent result to Redis, Flask fetch result from Redis
	
Celery structure: 
- Task
- Broker: 任务调度队列Redis
- worker
- Backend： 任务结果储存，Redis

创建requirements.txt
``pip freeze > requirement.txt``
迁移的时候 
``pip install -r requirements.txt`` 

```	
# ./config.py
CELERY_BROKER_URL = redis://localhost:6379/0
CELERY_RESULT_BACKEND = redis://localhost:6379/0
```
```
# ./__init__.py 
# 创建celery实例

def make_celery()
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
```
```
# ./routes/tasks.py 
# 创建后台任务
```
```
# ./routes/main.py
后台调用任务
delay()
apply_async()
```
```
# ./routes/main.py
状态查看
```
```
# 实现前端可视化
进度条
```

## 启动服务的步骤
ref: https://github.com/miguelgrinberg/flask-celery-example

### 创建并进入venv
```
sudo apt-get install python-pip
pip install virtualenv
virtualenv --version
virtualenv venv
source venv/bin/activate
```

### 在venv中安装requirements
``(venv) pip install -r requirements.txt``

### 启动redis
``redis-server redis.windows.conf``
或者使用默认config
``redis-server``

### 启动celery
``venv/bin/celery worker --app=app2.celery_worker.celery --loglevel=info``

- -A：指定celery实例 或者--app
- worker: 启动worker进程
- -l：指定log level，这里指定log level为debug level
- -f：指定输出的日志文件

### 启动Flask
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
venv/bin/flask run
```

# FAQ
### 什么叫在celery中使用Flask的上下文
就是app=Flask(____)实例化以后，要把celery加进去让他们到一起。为了避免循环引用的问题，方法是再app.py相同文件夹下写一个celery_worker.py
```python3
from app2 import create_app
from app2.tasks.celery_obj import celery

app = create_app()
app.app_context().push()
```
或者使用：flask_celery_helper: makes life better

### Factory模式（中文叫工厂函数)
即只有在创建Flask实例时，才会初始化各种扩展，这样可以动态的修改扩展程序的配置。
https://segmentfault.com/a/1190000009014285

### 注意secret key
must set secret key 

By default, Flask-Login uses sessions for authentication. This means you must set the secret key on your application, otherwise Flask will give you an error message telling you to do so. 
``os.urandom(16)`` // generate secret key 

# Flask学习笔记
再次学习，有新的内容和理解

**一个web app项目的基本功能**
- 用户登录系统（auth）：登录登出，连接数据库（sqlite, mysql）
- db（sqlalchemy包）（另包括init，migrate等）
- views，models，前端
- gunicorn作文http server

**项目结构组织**
- 把启动，配置，gunicorn放在根(/project)
- app，view，models，静态文件放在(/project/app)
- 把初始化db,app的函数另存一个地方，避免循环引用

**工具**
- db管理页面
- swaggerui
- gevent服务器：用来处理并发的

## 跳转
render_template, url_for

- referrer and next https://www.cnblogs.com/xiaxiaoxu/p/10403810.html
- 跳转到上个界面：
https://www.jianshu.com/p/451e7544a72a
- url_for()：给指定的函数构造url，接受参数：方法+一个字典（可以给方法传参，也可以作为query） 
http://docs.jinkan.org/docs/flask/api.html#flask.url_for
https://blog.csdn.net/baidu_36831253/article/details/78208650
- render_template()：渲染一个模板，接受参数（template_name_or_list, **context)） 

跳转到上个界面（登录可以用）
```python
@app.route('/hello')
def hello():
return "hello"

@app.route('/do_something_and_redirect')
def do_something():
    return redirect_back()

def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
```

## api设计

## 微信相关
https://github.com/zwczou/weixin-python#%E5%BE%AE%E4%BF%A1%E7%99%BB%E9%99%86

https://blog.csdn.net/skykingf/article/details/51882345

https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&t=resource/res_list&verify=1&id=open1419316505&token=&lang=zh_CN

## 用户session
### flask login
如果使用flask中的flask_login
这个模块中封装了session和cookie的处理
可以自己再login_manager中配置

### 自己写login并处理session

## flask migrate
https://www.jianshu.com/p/e4fc86fa21e8

修改库，表，想要保留原来的数据

第一次
```
flask db init
flask db migrate -m''
flask db upgrade
```

修改了库，表
```
flask db migrate
flask db upgrade
```

没有尝试过，大概会回滚
```
flask db migrate
flask db downgrade
```

---补充---
sqlite直接用migrate drop列会出问题，因为sqlite不能直接用``ALTER TABLE "Post" DROP COLUMN language``

