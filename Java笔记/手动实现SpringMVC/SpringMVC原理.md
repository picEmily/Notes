[TOC]

# Spring 中的一些概念

- 什么是Bean，IOC？

  - In Spring, the objects that form the backbone of your application and that are managed by the Spring IoC container are called beans. A bean is an object that is instantiated, assembled, and otherwise managed by a Spring IoC container.
  - 在 Spring 中，把 Spring IOC 容器管理的 **对象** 叫做 bean。
  - Spring IOC 容器实例化这些对象，装配（**为 bean 实例填充属性**）并管理它们。（**重要**）
  - @Component , @Repository , @ Controller , @Service , @Configuration 都是告诉 Spirng 我要把里面的对象注册到 Spring IOC 中成为 bean
  - IOC 就是通过 XML 配置，注解，config类来实例化 bean，而不是手动实例化（个人理解）

- Bean 装配过程：找到 bean--创建实例--装配  （没有自己读，待完善）

  - 1）在某一时刻（@Component , @Repository , @ Controller , @Service , @Configuration）Spring调用了 Bean工厂 的 getBean(beanName) 方法。

  - 2）getBean方法首先会调用Bean工厂中定义的getSingleton(beanName)方法，**来判断是否存在该名字的bean单例，若果存在则返回**，方法调用结束。

  - 3）否则，Spring会检查是否存在父工厂，如果有则返回，方法调用结束。

  - 4）否则，Spring 会检查该bean 定义（BeanDefinition实例，用来描述Bean结构，上篇文章讲到过，component-scan 扫描后，就是将beanDefinition实例放入Bean工厂，此时Bean还没有被实例化。）是否有依赖关系，如果有，执行1）步，获取依赖的bean实例。（将所有依赖都实例化并装配）

  - 5）否则，Spring会尝试创建这个bean实例，创建实例前，Spring会检查确定调用的构造器，并实例化该Bean。

  - 6）实例化完成后，**Spring会调用Bean工厂的populateBean方法来填充bean实例的属性，也就是我们前面提到的自动装配了**。populateBean方法便是调用了BeanPostProcessor实例来完成属性元素的自动装配工作。

  - 7）在元素装配过程中，Spring会检查被装配的属性是否存在自动装配的其他属性，然后递归调用getBean方法，直到所有@Autowired的元素都被装配完成。如在装配simpleController中的simpleService属性时，发现SimpleServiceImpl实例中存在@Autowired属性simpleDao，然后调用getBean（simpleDao）方法，同样会执行1）-7）整个过程。所以可以看成一个递归过程。

  - 8）装配完成后，Bean工厂会将所有的bean实例都添加到工厂中来。

    
    
    注：
    
    - 我们知道Spring MVC是**多线程单实例**的MVC框架，就是说，对于同一个Controller，只会生成一个实例来处理所有的请求，因此bean实例只会实例化一次，并被存放在工厂中，以供其他请求使用。
    - 整个过程递归，也就是说装配 bean 的过程中如果有依赖，那么会把依赖也先装配好
    
    

# SpringMVC 处理流程

SpringMVC 原理图简单

```
       	---request--→     					-----→ 
client 					C: DispatcherServlet		M: Service, Model, Dao
		←--response---			↑↓      	←----- 
							   ↑↓
							   ↑↓
							V: 渲染视图
```



SpringMVC 原理图细节（重新画）

<img src="C:\Users\wangd\Desktop\手动实现SpringMVC\SpringMVC流程图.png" style="zoom:80%;" />

## 过程

1. client 提交请求到 DispatcherServlet

2. DispatcherServlet 查询 HandlerMapping，返回 Handler

   - 根据 XML 配置，注解等查找

3. DispatcherServlet 根据查询的 Handler，选择合适的 HandlerAdapter (也就是 Controller) 执行 Handler

   - Spring 帮我们做一些额外工作：数据类型转化，数据验证等 （ preHandler？？？ ）

   - 执行 Handler 之前执行拦截器的 preHandler 方法
   - 执行 Handler 之后执行 postHandler 方法

4. HandlerAdapter 将 Controller 执行结果 ModelAndView 返回给 DispatcherServlet

5. DispatcherServlet 将 ModelAndView 发给 ViewResolver ，渲染视图

6. ViewResolver 将渲染结果 View 返回 DispatcherServlet

7. DispatcherServlet 结合 View 和 Model， 生成 response 并返回给 client

   - 将 Model 数据填充至 View 中

>  Notes: 
>
> - DispatcherServlet 与 client 直接联系（请求/响应）。
> - DispatcherServlet 和 各个组件沟通，分发任务，收集结果。
> - MVC 中的 C 指的是 DispatcherServlet，分发任务，收集结果。写代码时候的 controller 对应 M 中的 Handler

## 组件

框架提供的组件

- 前端控制器 DispatcherServlet
- 处理器映射器 HandlerMapping
- 处理器适配器 HandlerAdapter
- 视图解析器 ViewResolver

工程师开发

- 后端控制器 Handler：也就是 Controller
  - 处理用户请求，也就是具体的业务
  - 返回 ModelAndView 给 DispatcherServlet
- 视图 View：html，jsp等等

# 动手实现简单 SpringMVC

参考：

https://www.cnblogs.com/wyq178/p/9795640.html

https://www.cnblogs.com/moris5013/p/11010113.html

https://gitee.com/nanjunyu/ssm-example/blob/master/src/main/java/com/ssm/example/servlet/DispatcherServlet.java

## 注解实现

```java
// @Repository
@Target(ElementType.TYPE)			// 只能用在类上
@Retention(RetentionPolicy.RUNTIME)	 // 都是 Runtime
public @interface Repository {
	String value() default "";		// value 属性
}

// @Service
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
public @interface Service {
	String value() default "";
}

// @Controller
@Target({ElementType.TYPE,ElementType.METHOD})	// 用在类和方法上
@Retention(RetentionPolicy.RUNTIME)
public @interface Controller {
	String value() default "";
}

// @RequestMapping
@Target({ElementType.TYPE,ElementType.METHOD})	// 用在类和方法上
@Retention(RetentionPolicy.RUNTIME)
public @interface RequestMapping {
	String value() default "";				// "/api/v1/foo"
}
```

**自动织入功能**

```java
// @AutoWired
// 通过一个 IOC 识别这个装饰器并创造对象 
@Target(ElementType.FIELD)			// 只能用在类上
@Retention(RetentionPolicy.RUNTIME)	 // 都是 Runtime
public @interface AutoWired {
	String value() default "";		// value 属性
}
```

# 控制器 DispatcherServlet

这个是 SpringMVC 的**核心**

DispatcherServlet 是Spring的重要组件，继承自 HttpServlet（来自JDK）

注：该实现中 exception 都删了，简化一点

```java
public class MyDispatcherServlet extends HttpServlet {
    /**
     * 扫描的基准包
     */
    private String basePackage = "";
    /**
     * 包名
     */
    private List<String> packageNames = new ArrayList<>();
    /**
     * 注解名和类实例
     */
    private Map<String, Object> instanceMap = new HashMap<String, Object>();
    /**
     * 包名和注解名
     */
    private Map<String, String> nameMap = new HashMap<>();
    /**
     * url和方法
     */
    private Map<String, Method> urlMethodMap = new HashMap<>();
    /**
     * Method和包名
     */
    private Map<Method, String> methodPackageMap = new HashMap<>();
    @Override
        public void init(ServletConfig config) {
            getBasePackageFromConfigXml();
            scanBasePackage();
            pringInstance();
            springIoc();
            handleMapping();
    }
    
    private void getBasePackageFromConfigXml() {
        // ...
    }
    
    private void scanBasePackage() {
        // ...
    }
    
    private void pringInstance() {
        // ...
    }
    
    private void handleMapping() {
        // ...
    }
    
    /*
    * 处理GET请求
    */
    private void doPost() {
        // ...
    }
    
    /*
    * 处理POST请求
    */
    private void doGet() {
        // ...
    }
}
```

## getBasePackageFromConfigXml

从 Xml 配置中获取基础包

## scanBasePackage

扫描基础包，解析路径，获得目录下所有文件

## springInstance

遍历包下面的类，扫描类上面的注解。找到特定注解（@Controller、@Service、@Repository），利用反射（获取注解上的配置参数）生成该类的实例，添加到 instanceMap

```java
    private void springInstance () {
        if (packageNames.size() < 1) {
            return;
        }
        for (String packageName : packageNames) {
            Class<?> fileClass = Class.forName(packageName);
            if (fileClass.isAnnotationPresent(Controller.class)) {
                // Controller 注解的类
                Controller controller = fileClass.getAnnotation(Controller.class);
                final String controllerName = Controller.value();
                instanceMap.put(controllerName, fileClass.newInstance());	// 创建实例
                nameMap.put(packageName, controllerName);
            } else if (fileClass.isAnnotationPresent(Service.class)) {
                final Service service = fileClass.getAnnotation(Service.class);
                final String serviceName = service.name();
                instanceMap.put(serviceName, fileClass.newInstance());
                nameMap.put(packageName, serviceName);
            } else if (fileClass.isAnnotationPresent(Repository.class)) {
                final Repository repository = fileClass.getAnnotation(Repository.class);
                final String repositoryName = repository.name();
                instanceMap.put(repositoryName, fileClass.newInstance());
                nameMap.put(packageName, repositoryName);
            }
        }
    }
```

## springIoc 

springIoc的注入：该方法的目的主要是遍历instanceMap,找到有@Controller、@Service、@Repository中的成员字段上有@AutoWired的注解，然后获取这个注解，**利用反射机制，实例化这个成员变量**。

Sping 中实际是实现 BeanFactory 来来做到自动装配 （通过注解实例化对象）

Q: 什么是反射机制

A: 就是一组API，获得被注解对象的类的信息

	- ``isAnnotationPresent()`` 判断是否有注解
	- ``getAnnotation()``
	- ``getClass()`` or ``.class`` 获取 class 对象
	- ``getName()``, ``getFields()``, ``getMethod()`` / ``getDeclaredMethod()``
	- ...

```java
private void springIoc() {
        for (Map.Entry<String, Object> annotationNameAndInstance : instanceMap.entrySet()) {		// 找到有@Controller、@Service、@Repository 标注的类
            final Field[] fields = annotationNameAndInstance.getValue().getClass().getDeclaredFields();	// 反射机制找到被注解类的所有 fields
            for (Field field : fields) {
                if (field.isAnnotationPresent(AutoWired.class)) {									// 如果注解是 AutoWired
                    // 成员变量(fields)的实例化
                    final String myInstanceName = field.getAnnotation(AutoWired.class).value();		// 获得该注解的属性 value 
                    field.setAccessible(true);
                    field.set(annotationNameAndInstance.getValue(), instanceMap.get(myInstanceName));	// key：注解名 value：实例
                }
            }
        }
    }
```

## handlerMapping

```java
/**
* 处理请求的url和method
* 处理 @RequestMapping 注解
*/
private void handlerMapping() {

    if (packageNames.size() < 1) {
        return;
    }

    for (String packageName : packageNames) {

        final Class<?> fileClass = Class.forName(packageName);
        final Method[] methods = fileClass.getMethods();			// 得到类的所有方法（一般就是@Controller 层）
        final StringBuffer baseUrl = new StringBuffer();
        
        // 类被 @RequestMapping 修饰
        if (fileClass.isAnnotationPresent(RequestMapping.class)) {
            RequestMapping request = (RequestMapping) fileClass.getAnnotation(RequestMapping.class);
            baseUrl.append(request.value());
        }
        
        // 方法s被 @RequestMapping 修饰
        for (Method method : methods) {
            if (method.isAnnotationPresent(RequestMapping.class)) {		// 当有方法被 @RequestMapping 修饰
                final RequestMapping request = method.getAnnotation(RequestMapping.class);
                baseUrl.append(request.value());

                urlMethodMap.put(baseUrl.toString(), method);
                methodPackageMap.put(method, packageName);
            }
        }
    }
}
```



## 处理请求

```java
/**
* 具体的处理请求的方法
* @param req
* @param resp
* @throws ServletException
* @throws IOException
*/
@Override
protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
    final String requestURI = req.getRequestURI();
    final String contextPath = req.getContextPath();			// 服务器地址
    final String path = requestURI.replaceAll(contextPath, "");	// 得到api /api/v1/foo
    //根据请求的路径反向获取方法
    final Method method = urlMethodMap.get(path);
    if (null != method) {
        //获取包名
        final String packageName = methodPackageMap.get(method);
        //根据包名获取到Controller的名字
        final String controllerName = nameMap.get(packageName);
        //根据controller的名字得到控制器
        Object controller =  instanceMap.get(controllerName);
        try {
            method.setAccessible(true);
            method.invoke(controller);
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        } catch (InvocationTargetException e) {
            e.printStackTrace();
        }
    }
}
```



