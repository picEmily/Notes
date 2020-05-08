# 参考
http://www.ruanyifeng.com/blog/2014/05/restful_api.html
https://zhuanlan.zhihu.com/p/91240556

# 理解RESTful API架构
- 主要矛盾：如何开发在互联网环境中使用的软件

## 什么是RESRful API架构
- 一种互联网软件架构
- REST，即Representational State Transfer的缩写 （表现层状态转化）

含义
- 资源（Resources）：网络上的实体，比如文本，图像，歌曲，可以用URI定位（统一资源定位符）
- 表现层（Representation）：资源的表现形式，比如html，JSON，PNG等。在HTTP请求头中用Accept和Content-Type指定。
- 状态转化（State Transfer）：HTTP是无状态协议，所有状态都保存在服务器，只能通过HTTP协议来改变服务器的状态(GET, PUT, POST, DELETE)。

## RESTful 原则
- C-S架构：数据存储在server端，client端只需要使用。两端单独开发，彻底分离。
- 无状态：无需保存客户端的状态。客户端在每次请求的时候带上充分的信息让服务端识别。
- 统一的接口：客户端只需关注接口的实现。
	- 资源识别：URI
	- 请求动作：http method
	- 响应信息：通过返回状态码表示请求的结果
- 一致的数据格式：XML，JSON，状态码
- 可缓存
- 服务端可选择下发一些代码让客户端执行（例如javascript代码）


# RESTful API设计指南

## 常见错误
- 最常见的一种设计错误，就是URI包含动词。因为"资源"表示一种实体，所以应该是名词，URI不应该有动词，动词应该放在HTTP协议中。
	- 举例来说，某个URI是``/posts/show/1``，其中show是动词，这个URI就设计错了，正确的写法应该是``/posts/1``，然后用**GET**方法表示show。
	- 如果某些动作是HTTP动词表示不了的，你就应该把动作做成一种资源。比如网上汇款，从账户1向账户2汇款500元，错误的URI是：
	```
	POST /accounts/1/transfer/500/to/2
	```
	正确的写法是把动词transfer改成名词transaction，资源不能是动词，但是可以是一种服务：
	```
	POST /transaction HTTP/1.1
	Host: 127.0.0.1
　　from=1&to=2&amount=500.00
	```

# 实践
http://www.ruanyifeng.com/blog/2018/10/restful-api-best-practices.html
- 不要出现动词
- 用复数

Q：状态