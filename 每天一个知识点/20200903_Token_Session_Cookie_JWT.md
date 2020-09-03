[TOC]

参考：https://mp.weixin.qq.com/s/OhOeEfm0ITvkjNhWhKhuEw

# 认证、授权和凭证

## 定义

- 认证(Authentication)：**验证用户当前身份**
  - 可以是用户名，密码
  - 邮件验证，手机验证码
- 授权(Authorization): **用户授予第三方应用访问该用户某些资源的权限**
  - 授权微信小程序可以访问我的联系人，地址，相册等
  - 实现授权的方式：cookie，session，token，OAuth（微信是OAuth2）
- 凭证(Credentials): **实现认证和授权的前提**是需要一种**媒介（证书）** 来标记访问者的身份
  - 用户成功登陆后网站会给用户一个令牌（token），令牌用来表明自己的身份
  - http是无状态的，通过令牌可以避免每个操作都登录

## 常见**前后端鉴权方式**

1. Session-Cookie
2. Token 验证（包括 JWT，SSO）
3. OAuth2.0（开放授权）

# Cookie 和 Session

**HTTP 是无状态的协议（对于事务处理没有记忆能力，每次客户端和服务端会话完成时，服务端不会保存任何会话信息**）：每个请求都是完全独立的，服务端无法确认当前访问者的身份信息，无法分辨上一次的请求发送者和这一次的发送者是不是同一个人。所以服务器与浏览器为了进行会话跟踪（知道是谁在访问我），就必须主动的去维护一个状态，这个状态用于告知服务端前后两个请求是否来自同一浏览器。而这个状态需要通过 cookie 或者 session 去实现。

## Cookie

- **cookie 存储在客户端：** cookie 是服务器发送到用户浏览器并保存在本地的一小块数据，它会在浏览器下次向同一服务器再发起请求时被携带并发送到服务器上。
- **cookie 是不可跨域的：** 每个 cookie 都会绑定单一的域名，无法在别的域名下获取使用，**一级域名和二级域名之间是允许共享使用的**（**靠的是 domain）**。

> 跨域：cross-origin 不同的一级二级域名
>
> 也就是说 A 网站是无法访问 B 网站留下的 cookie

### **使用 cookie 时需要考虑的问题**

- 因为存储在客户端，容易被客户端篡改，使用前需要验证合法性
- 不要存储敏感数据，比如用户密码，账户余额
- 使用 httpOnly 在一定程度上提高安全性
- 尽量减少 cookie 的体积，能存储的数据量不能超过 4kb
- 设置正确的 domain 和 path，减少数据传输
- **cookie 无法跨域**
- 一个浏览器针对一个网站最多存 20 个Cookie，浏览器一般只允许存放 300 个Cookie
- **移动端对 cookie 的支持不是很好，而 session 需要基于 cookie 实现，所以移动端常用的是 token**

## Session

- session 是另一种记录服务器和客户端会话状态的机制
- **session 存在服务端**
- session 是基于 cookie 实现的，**sessionId 会被存储到客户端的cookie 中**

<img src="C:\Users\wangd\Desktop\每天一个知识点\session流程.webp" style="zoom: 67%;" />

> 图中的流程是把 sessionID 存在 Cookie 中，服务器从 Cookie 中获取 SessionID，然后查找存在服务端中的session 信息，例如 token 过期了没有。游客模式一般都是用了这样的 cookie + session。
>
> 我个人理解的话也不一定要配合使用，比如我可以把 userID 和 sessionID 存数据库，某个 User 登录了我也能直接查 session，但是登录状态可能不太行，只能记录例如上次用户退出位置的信息。

### **使用 session 时需要考虑的问题**

- 将 session 存储在服务器里面，当用户同时在线量比较多时，**这些 session 会占据较多的内存**，需要在服务端定期的去清理过期的 session。
  - session 可以做持久化本地持久化或者数据库服务器；或者用缓存：本地缓存，redis缓存都可以
  - session 设置失效时间也是为了防止太多了存不下
- 当网站采用**集群部署**的时候，会遇到多台 web 服务器之间如何做 session 共享的问题。因为 session 是由单个服务器创建的，但是处理用户请求的服务器不一定是那个创建 session 的服务器，那么该服务器就无法拿到之前已经放入到 session 中的登录凭证之类的信息了。
- 当多个应用要共享 session 时，除了以上问题，还会遇到跨域问题，因为不同的应用可能部署的主机不一样，需要在各个应用做好 cookie 跨域的处理。
- **sessionId 是存储在 cookie 中的，假如浏览器禁止 cookie 或不支持 cookie 怎么办？** 一般会把 sessionId 跟在 url 参数后面即重写 url，所以 session 不一定非得需要靠 cookie 实现
- **移动端对 cookie 的支持不是很好，而 session 需要基于 cookie 实现，所以移动端常用的是 token**

### 分布式 session 共享方案

- 复制：整个集群都一直同步 session
- IP 绑定：**采用 Ngnix 中的 ip_hash 机制，将某个 ip的所有请求都定向到同一台服务器上，即将用户与服务器绑定。**
- 共享 session：比如 redis 集群，memcached 集群来缓存session。数据库服务器持久化也行。总之就是不是存在某个服务器自己那里。

## Cookie 和 Session 对比

- 相似点：

  - 都是为了解决 Http 无状态属性带来的困难，存储了一些状态信息。
  - 都能存一些信息

- 不同点：

  - 主要不同：1) cookie 在客户端，session 在服务端 2) 存的东西不太一样：？？？
  - 次要不同：

  > - **安全性：** Session 比 Cookie 安全，Session 是存储在服务器端的，Cookie 是存储在客户端的。
  >
  > - **存取值的类型不同**：Cookie 只支持存字符串数据，想要设置其他类型的数据，需要将其转换成字符串，Session 可以存任意数据类型。
  > - **有效期不同：** Cookie 可设置为长时间保持，比如我们经常使用的默认登录功能，Session 一般失效时间较短，客户端关闭（默认情况下）或者 Session 超时都会失效。
  > - **存储大小不同：** 单个 Cookie 保存的数据不能超过 4K，Session 可存储数据远高于 Cookie，但是当访问量过多，会占用过多的服务器资源。

# Token

## Access Token

- **访问资源接口（API）时所需要的资源凭证**

- **简单 token 的组成：** uid(用户唯一的身份标识)、time(当前时间的时间戳)、sign（签名，token 的前几位以哈希算法压缩成的一定长度的十六进制字符串）

- **特点：**

- - **服务端无状态化、可扩展性好**
  - **支持移动端设备**
  - 安全
  - 支持跨程序调用

- **token 的身份验证流程：**

![](C:\Users\wangd\Desktop\每天一个知识点\token验证流程.webp)



获取 token

1. 客户端使用用户名跟密码请求登录；服务端收到请求，去验证用户名与密码
2. 验证成功后，服务端会签发一个 token 并把这个 token 发送给客户端
3. 客户端收到 token 以后，会把它存储起来，比如放在 cookie 里或者 localStorage 里

使用 token

1. 客户端每次向服务端请求资源的时候需要带着服务端签发的 token
2. 服务端收到请求，然后去验证客户端请求里面带着的 token ，如果验证成功，就向客户端返回请求的数据

怎么使用？

- **每一次请求都需要携带 token，需要把 token 放到 HTTP 的 Header 里**
- **基于 token 的用户认证是一种服务端无状态的认证方式，服务端不用存放 token 数据。用解析 token 的计算时间换取 session 的存储空间，从而减轻服务器的压力，减少频繁的查询数据库**
- **token 完全由应用管理，所以它可以避开同源策略**

> token 可以解析出 uid，timestamp 等信息

## Refresh Token

refresh token 是专用于刷新 access token 的 token。如果没有 refresh token，也可以刷新 access token，但每次刷新都要用户输入登录用户名与密码，会很麻烦。有了 refresh token，可以减少这个麻烦，客户端直接用 refresh token 去更新 access token，无需用户进行额外的操作。

(???) 为什么不把 access token 时间延长？？？

<img src="C:\Users\wangd\Desktop\每天一个知识点\refresh_token.webp" style="zoom:80%;" />

Notes：

session 和 token 某些功能重合：都能用来验证权限，但是：

- session 存的是用户的状态，比如登陆的状态。session 要保密的，不能被第三方拿到。
- token 是一个令牌，服务器通过这个令牌判断用户有什么权限

## JWT (JSON Web Token)

说白了就是 token 的一种，但是用了加密（对称或不对称）。

JWT 还能把一些信息一起加密进去，不需要额外再查 session

定义

- JSON Web Token（简称 JWT）是目前最流行的**跨域认证**解决方案。
  - 放在 header / URL/ Request Body里，不放在 cookie 里，可以跨域
- 是一种**认证授权机制**。
- JWT 是为了在网络应用环境间**传递声明**而执行的一种基于 JSON 的开放标准（RFC 7519）。JWT 的声明一般被用来在身份提供者和服务提供者间传递被认证的用户身份信息，以便于从资源服务器获取资源。比如用在用户登录上。
- 可以使用 HMAC 算法或者是 RSA 的公/私秘钥对 JWT 进行签名。因为数字签名的存在，这些传递的信息是可信的。

和 token 的区别

- Token：服务端验证客户端发送过来的 Token 时，还需要查询数据库获取用户信息，然后验证 Token 是否有效。
- JWT：将 Token 和 Payload 加密后存储于客户端，服务端只需要使用密钥解密进行校验（校验也是 JWT 自己实现的）即可，**不需要查询或者减少查询数据库，因为 JWT 自包含了用户信息和加密的数据。**



### **使用 token 时需要考虑的问题**

- 如果你认为用数据库来存储 token 会导致查询时间太长，可以选择放在内存当中。比如 redis 很适合你对 token 查询的需求。
- **token 完全由应用管理，所以它可以避开同源策略** ？？？
- **token 可以避免 CSRF 攻击(因为不需要 cookie 了)**
- **移动端对 cookie 的支持不是很好，而 session 需要基于 cookie 实现，所以移动端常用的是 token**





