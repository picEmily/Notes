# 准备工作
- 一个趁手的IDE
- JDK
- maven
- 文档：https://spring.io

Tutorial：
https://spring.io/guides
https://start.spring.io/
https://spring.io/quickstart
https://spring.io/guides/gs/spring-boot/
https://spring.io/guides/gs/rest-service/

**了解tomcat，servlet，spring，jsp**
参考：https://www.jianshu.com/p/7f27b2362f62
- jsp：java server pages，结合html，能被渲染成网页（我理解类似flask的jinja2）
- Tomcat：Tomcat是一个能够监听TCP连接请求，解析HTTP报文，将解析结果传给处理逻辑器、接收处理逻辑器的返回结果并通过TCP返回给浏览器的一个框架。（gunicorn，wsgi in python）
	- 也就是服务器，通过TCP接受/返回HTTP报文
	- Tomcat是多线程的，每一个请求都是一个线程
	- 逻辑处理器就是servlet
- Servlet：处理HTTP请求（``service()``方法对HTTP请求分类，然后调用``doGet()``, ``doPost()`` 等方法）
	- Servlet被Tomcat创建、调用和销毁
	- Servlet是单个的实例
	- Tomcat会传过来两个参数：（``HttpServletRequest request``, ``HttpServletResponse response``）。我们通过 ``HttpServletRequest`` 对象获取请求信息，通过 ``HttpServletResponse`` 对象向Tomcat返回数据。
- Spring：本质上是servelet的实现
	- 在``init``中通过类加载器检索所有的``@Controller``、``@Service``等类，然后通过反射实例化类，通过反射向类中注入实例依赖。著名顶顶的IOC是什么？其实，它就是一个HashMap！！！{key=类长名，value=实例对象}。

**spring/spring framework/spring boot/spring cloud的区别**

- spring 包含以下所有，是一个bean管理的容器，包括很多项目
- spring framework：框架（编程和配置模型），开发人员更专注于业务逻辑
- spring boot：快速启动最小化配置的spring 应用
	- 自动配置 Spring
- spring cloud： spring cloud是基于spring boot 的**微服务**解决方案
- springmvc：基于spring的web框架

**Maven VS Gradle**
https://gradle.org/maven-vs-gradle/
- 都是项目自动构建工具
	- 编译，单元测试，静态代码分析，发布版本，部署 等等等等
- Maven更旧，是目前的标准，基于XML，略复杂
- Gradle更新，目前用于Android，基于Groovy语言，更简单

# Spring Framework
https://docs.spring.io/spring/docs/current/spring-framework-reference/

笔记中的章节注释出自
《Spring实战》 第四版 Craig Walls 著

入门水平：
- Spring 的两大核心：依赖注入，面向切面编程
	- 注入依赖和切面都通过配置文件进行
	- 解耦合
- Spring 容器：BeanFactory，应用上下文
	- Spring 容器负责创建，装配，管理整个生命周期
- Spring Template 的使用（比如查询数据库的 ``jdbcTemplate``）

> 在spring 中可以说我们实现的是CD机，往里面插入CD就是装配。

关键词：
- POJO：普通的 java 类
	- Spring 避免继承spring提供的API，又叫做最小入侵。Spring 中依旧使用POJO。
- 依赖注入DI（依赖是作为参数注入进去的）
	- **对象只通过接口来表明依赖关系**，调用的时候再传入对接口的实现（**注入**）
	- 减小对象间依赖关系（慢慢体会）
	- 装配（装在Bean）：创建应用组件之间的协作。在配置文件中有两种方式：XML，java。在 ``main()`` 中加载
- 面向切面的编程：
	- 将非业务模块拿出来（比如log）


## Spring 模块
20个模块，分为6类

**Spring 核心容器**
最核心的部分
包括Bean工厂，上下文

**面向切面编程**
AOP
Aspects

**数据访问与集成**
JDBC->ORM

**Web与远程调用**
？？

**Instrumentation**
？？

**测试**

## 装配Bean
**Bean管理**
1.2.2 bean的生命周期（从创建到销毁）
- 声明Bean
- 构造器注入和Setter方法注入
- 装配Bean
- 控制Bean的创建和销毁

**装配Bean** （细节第二章）
推荐顺序：自动化> Java代码装配>XML装配
- 自动化装配（隐式）
	- **自动装配**就是Spring自动满足bean依赖的一种方法，在满足依赖的过程中，会在spring应用上下文中匹配某个bean需求的其他bean
	- 需要启用**组件扫描**和**自动装配**（细节看2.2）
	- ``@Component``, ``@ComponentScan``, ``@Autowired``
- Java中配置（显式）
- XML中配置（显式）

### sample DI
设想一个场景：
- ``CDPlayer``类：播放器
- ``CompactDisc``接口：CD
- 实现``CompactDisc``：比如某张专辑《CaoNiMa》

我们需要将一个CompactDisc注入到CDplayer中

**创建可被发现的bean**
```java
/*
 * CompactDisc接口
 */
public interface CompactDisc {
	void play();
}
```

```java
/*
 * 实现 CD，需要@Component注解
 * 该类为组件类，告知Spring要为这个类创建Bean（自动，不需要配置）
 */
@Component
public class CaoNiMa implements CompactDisc {
	private String title = "CaoNiMa";
	private String author = "Jay";

	public void play() {
		System.out.println("Playing " + title);
	}
}
```

**启用组件扫描**
```java
/*
 * @ComponentScan启用注解扫描，默认扫描包内所有子包，查找带有@Component注解的类
 */

@ComponentScan
public class CDPlayerConfig {

}
```

```java
/*
 * @AutoWired注解表示：创建CDPlayer的时候，通过构造器实例化，会传入一个可设置给CompactDisc类型的bean
 */
public class CDPlayer {
	private CompactDisc cd;
	
	/*
	 * 不需要new CompactDisc cd;
	 */
	@AutoWired
	public CDPlayer(CompactDisc cd) {
		this.cd = cd;
	}

	public void play() {
		cd.play();
	}
}
```

## 面向切面编程AOP
Spring的四种AOP支持：
- 基于代理的Spring AOP？？？
	- Spring 提供的 AOP 框架能满足大多是情况使用
- 纯POJO切面
	- 需要配置XML
- ``@AspectJ``注解驱动
	- 实现了AspectJ切面的部分功能
- 注入式AspectJ切面

> 基于注解的配置 >> 基于java的配置 >> 基于XML的配置
> PS：我看教程的话感觉 ``@AspectJ`` 最方便用

**横切关注点**：多种功能（log，安全，事务管理等），希望与业务分开。模块化为**特殊的类**，被称为**切面**
**面向切面编程**：仍然定义通用功能，但是通过声明的方式定义功能在哪以何种方式使用，**无需修改受影响的类**

**AOP术语**
- 通知：何时执行工作？
	- 前置，后置，返回，异常，环绕
- 连接点：连接点是一个应用执行过程中能够插入一个切面的点（说人话就是我们插入切面代码的地方）
	- 可以是调用方法时、抛出异常时、甚至修改字段时
	- 切面代码可以利用这些点插入到应用的正规流程中
- 切点
	- 匹配到的类和方法名称（PS：我个人理解为类似 ``findElementById()`` 类似的query功能）
	- ``execution(* [Package Name].[Class Name].[Method Name]([args type])) && args([args])``
- 切面：通知 + 切点
- 引入
- 织入



# 使用 Spring boot 简化开发
- 使用Spring Boot Starter添加项目依赖
	- 将依赖合并，一次性添加到Maven或Gradle构建中
- 自动化的 bean 配置 
- Groovy 与 Spring Boot CLI （我觉得可以暂时略？？？） 
- Spring Boot Actuator

## Guides
### Sample 1
https://spring.io/guides/gs/rest-service/
```
// HTTP requests are handled by a controller.
@RestController 

// mapping 定义路由和方法
@GetMapping("/greeting")
@PetMapping("/greeting")
@RequestMapping(method=GET)

// Response 都是对象
// MappingJackson2HttpMessageConverter() 会将对象转换成Json
return [Object]

// The main() method uses Spring Boot’s 
// SpringApplication.run() method to launch an application
@SpringBootApplication 包含
@Configuration，@EnableAutoConfiguration，@ComponentScan
```

运行：
```
# Gradle
./gradlew bootRun 
OR
./gradlew build
java -jar build/libs/gs-rest-service-0.1.0.jar

# Maven
./mvnw spring-boot:run
OR
./mvnw clean package
java -jar target/gs-rest-service-0.1.0.jar
```

maven-wrapper: maven 继续简化
https://www.jianshu.com/p/dcc563b9bf4c

安装位置：``~/.m2/wrapper/dists/``

项目关于maven wrapper的配置文件：``./.mvn/maven-wrapper.properties``

不知道咋配置就去阿里云手动下
https://maven.aliyun.com

### Sample 2
《Spring实战》21.2章节
简单的联系人列表
- 允许输入联系人信息（名字，电话，Email）
- 能列出之前输入的所有联系人信息

技术：
- Spring MVC控制器
- Thymeleaf 模板？？？
- Repository
- Spring JdbcTemplate

### Sample 3
https://www.hangge.com/blog/cache/detail_2454.html#

### Sample 4
Auth 系统
https://www.cnblogs.com/dranched/p/9326227.html

@Autowired annotation 的作用
@RestController 返回对象
@Controller 加载页面模板

### Sample 5
验证登录：拦截器
登录请求--->拦截器判断session--->后台验证/设置session--->返回结果

### Sample 6
Spring Security 设置用户权限
增加 Interceptor层

# Spring Boot 项目分层结构
参考：
https://blog.csdn.net/wyx0224/article/details/81190792
https://www.cnblogs.com/tooyi/p/13340374.html

- 首先，最底层的就是**dto**层，dto层就是所谓的**Model**，dto中定义的是实体类，也就是.class文件，该文件中包含实体类的属性和对应属性的get、set方法；
- 其次，是**dao**层（dao层的文件习惯以**Mapper**命名），dao层会调用dto层，dao层中会定义实际使用到的方法，比如增删改查。一般在dao层下还会有个叫做sqlmap的包，该包下有xml文件，文件内容正是根据之前定义的方法而写的SQL语句；
- 之后，到了**service**层，service层会调用dao层和dto层，service层也会对数据进行一定的处理，比如条件判断和数据筛选等等；
- 最后，是**controller**层，controller层会调用前面三层，controller层一般会和前台的js文件进行数据的交互， controller层是前台数据的接收器，后台处理好的数据也是通过controller层传递到前台显示的。

# 踩坑
**start code**
- 可以从网上下载 https://start.spring.io/
- 只有专业版IDEA才能直接在IDEA里使用 spring initializr

**更换源地址：**
根目录下 ``~/.m2/`` 文件夹下新建 ``settings.xml``，然后添加阿里云源
或者右键 ``pom.xml``-> Maven -> Create settings.xml
```
<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0
                      http://maven.apache.org/xsd/settings-1.0.0.xsd">
  <localRepository/>
  <interactiveMode/>
  <usePluginRegistry/>
  <offline/>
  <pluginGroups/>
  <servers/>
  <mirrors>
    <mirror>
    <id>aliyunmaven</id>
    <mirrorOf>central</mirrorOf>
    <name>aliyun maven</name>
    <url>https://maven.aliyun.com/repository/public </url>
    </mirror>
  </mirrors>
  <proxies/>
  <profiles/>
  <activeProfiles/>
</settings>
```  

**Maven依赖问题**
1. 如果是 https://start.spring.io/ 上导入的话，可以选择依赖，会自动写到 ``pom.xml`` 中。
	- 小Web项目需要: Spring Web（RESTful，SpringMVC，Apache Tomcat）, Spring Data JPA (数据库)/Mybatis
2. 右键``pom.xml``->Maven->Reimport
3. 还解决不了就在``pom.xml``中添加需要的标签 ``<dependency>...</dependency>``，然后再reimport


TODO: https://www.jianshu.com/p/f57db8b29be9

**Spring 数据库问题**
- 在setting->plugin中下载 ``database navigator``或者 ``database tools and sql``
	- Spring 中数据库介绍：https://www.baeldung.com/java-in-memory-databases
	- Spring 中Sqlite配置起来有点复杂：https://www.baeldung.com/spring-boot-sqlite
- Spring中常用的ORM方案：Hibernate，JPA
- 官方guide
	- H2:一个小巧，简洁，java开发的数据库 https://spring.io/guides/gs/accessing-data-rest/ 
	- MySQL https://spring.io/guides/gs/accessing-data-mysql/

**Controller相关**
https://www.cnblogs.com/guo-xu/p/11203740.html
- 区别``@Controller`` and ``@RestController``
- 如何渲染html，JSP

**Request method 'POST' not supported**
前端Form表单直接提交POST，Spring ``doDispatch()`` 有问题？？？（问题在哪）（js 提交是否可行？？）
1. 后端不用POST渲染静态页面，而是重定向