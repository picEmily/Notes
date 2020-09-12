# CSS 
**CSS implement details**
**CSS selector:** (class, tag, id...) CSS tie styling information to the HTML elements; CSS selector will use the more **specific** one. 
- div { color: red} tag
- .class1 { color: red} class
- div.class1 { color: red} tag+class
- #span2 {color: red} id
- #span2 .class1 { color: red} &&

## Position
- **fixed:** positions the element with respect to the viewport ; fixed means that the element is fixed in place as scrolling occurs
- **absolute:** positions the element with respect to its closest ancestor
- relative: 
- **relative:** The element is positioned relative to its static/default/normal position in the document flow.
## Unites
- **Absolute Lengths:** 
	- fixed, appear as exactly that size. Absolute length units are not recommended for use on screen, because screen sizes vary so much. However, they can be used if the output medium is known, such as for print layout.
	- cm, mm, in, px, pt, pc
- **Relative Lengths:**
	- specify a length relative to another length property. Relative length units scales better between different rendering mediums.
	- em, ex, ch, rem, vw, vh, vmin, vmax, %(relative to the parent element)

## Display
- **block:** Block elements start on a new line and take up the entire horizontal width available by
default. They can also have a specified height and width.
- **inline:** Inline elements take up as much space as their content, or in other words they only take up as much space as necessary. This allows them to be placed along the same horizontal line, wrapping around if
necessary.
- **inline-block:** 
	- Compared to inline, inline-block allows to set a width and height on the element. the top and bottom margins/paddings are respected;
	- Compared to block, inline-block does not add a line-break after the element, so the element can sit next to other elements.
- **flex:** 
	- The Flexible Box Layout Module, makes it easier to design flexible responsive layout structure without using float or positioning.
	- 可以设置flex-direction, flex-wrap, justify-content, align-items, align-content

## Box
## Width Height
 \<b> and \<i> to be replaced by \<strong> and \<em>. Or with CSS.

# DOM
- HTML document exposed as a **collection of JavaScript objects and methods**
	- The Document Object Model (DOM)
- JavaScript can query or modify the HTML document
- Accessible via the JavaScript global scope, aliases:
	- window	
	- this (When not using 'use strict'; )

## DOM Nodes and hierarchy
- Rooted at window.document
- Walk DOM hierarchy (not recommended)
	element = document.body.firstChild.nextSibling.firstChild;
	element.setAttribute(…
- Use DOM lookup method. An example using ids:
	HTML: \<div id="div42">...</div>
	element = document.getElementById("div42");
	element.setAttribute(…
## DOM communicates to JavaScript with Events 
### Specifying the JavaScript of an Event
- Option #1: in the HTML:
\<div onclick="gotMouseClick('id42'); gotMouse=true;">...</div>
- Option #2: from Javascript using the DOM:
element.onclick = mouseClick;
or
element.addEventListener("click", mouseClick);

### Capturing and Bubbling Events
- ``element.addEventListener(eventType, handler, true); `` :从外到内（Capture phase）
- ``element.addEventListener(eventType, handler, false);`` :从内到外（Bubble phase）（如果不指定第三个参数默认false）
- Correct Answer(Capture Phase) with Correct Explanation (capture phase is always **prioritized** over bubble no matter what)

**event**
```
function callback(event) {
	console.log(event.target.id + ' ' + event.currentTarget.id)
}
```
**event 分析：**
- 这个callback就是实例中的handler参数（handler是一个function），callback的参数event是addEventListener()中的eventType，比如我这里写click那么event就是click。
- event.target就是我点击的那个元素，event.currentTarget是会Bubbling或者Capturing的元素
- 每次点击任意一个元素，就从最外部开始capture这个元素，直到找到这个元素。如果event registered as true， 在capturing阶段触发事件，vice versa。
> [Bubbling and Capturing](http://www.calledt.com/target-and-currenttarget/)
> [target和currentTarget](https://www.cnblogs.com/yewenxiang/p/6171411.html)

### Modify  

# URL
![sample](https://img-blog.csdnimg.cn/20190213063322863.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dhbmd6aWhhaGFoYQ==,size_16,color_FFFFFF,t_70)
- scheme: identifies protocol used to fetch the content.
- Host name: name of a machine to connect to
- Server's port number: allows multiple servers to run on the same machine
- path or Hierarchical portion, used by server to find content
	- Let's say if your browsing /cream-cakes/ then you have a link on the page that has blah.html without the forward flash its going to attempt to visit page /cream-cakes/blah.html while with the forward flash it'll assume you mean the top level which will be domain.com/blah.html.
	- ![eg1](https://img-blog.csdnimg.cn/20190212133155517.PNG)
	- I. http://www.example.com/starts/with/a/slash（with a slash: absolute URL）
		II. http://www.example.com/initialpage/no/starting/slash (W/O a slash, relative URL)
- Query parameters, provides additional parameters
	- Any character in a URL other than A-Z, a-z, 0-9, or any of -_.~ must be represented as %xx, where xx is the hexadecimal value of the character:
- Fragment Have browser scroll page to fragment
	- Fragment used on browser only, not on the server. 
	
**URL作用：** 
- loading page in web browser
- another scheme besides http (e.g. mailto, file, ftp, ssh), and/or
another port besides 80.
- Other answers: 1) Locating server API to fetch data 2) Locating page resources (images, stylesheets)

**URI** (Uniform Resource Identifier) vs. **URL** (Uniform Resource Locator):  [reference](https://stackoverflow.com/questions/176264/what-is-the-difference-between-a-uri-a-url-and-a-urn)
- All URLs are URIs
- A URI can be further classified as a locator, a name, or both. The term "Uniform Resource Locator" (URL) refers to the subset of URIs that, in addition to identifying a resource, provide a means of locating the resource by describing its primary access mechanism 

# JavaScript
## Prototype Mystery
[why use prototype](https://www.jianshu.com/p/e3b6ef04eda4)
```
function Foo(y) { this.y = y; };
Foo.prototype.x = 10;
FOo.prototype.calculate = function () { … };
let b = new Foo(20);
let c = new Foo(30);
```

![图解](https://img-service.csdnimg.cn/img_convert/f5bf7860ec68d5e9c7901d4575d28801.png)
> [参考](https://blog.csdn.net/zeping891103/article/details/79215201)
> [prototype and proto](https://segmentfault.me/2017/01/22/proto%E4%B8%8Eprototype%E7%9A%84%E5%85%B3%E7%B3%BB/)
```
// prototype trick

function Jeep() {
    this.organization = "DaimlerChrysler";
}
Jeep.prototype.color = "blue";
var blue = new Jeep();
console.log(blue.organization);  
console.log(blue.color); // 顺着原型链向上找，自己的proto没有，找到了自己的爸爸的color
var red = new Jeep();
red.color = "red";
console.log(red.organization); 
console.log(red.color);  // 自己的原型链上有，所以是red不是blue
Jeep.organization = "Chrysler";
console.log(Jeep.organization); // 只改了自己的，没有改prototype
Jeep.prototype.color = "green"; // 改了prototype
console.log(blue.organization); 
console.log(blue.color); // 因为自己没有color属性，所以是green
console.log(red.organization); 
console.log(red.color); // 自己有color，所以是green

Jeep.prototype.organization = "Chrysler";
console.log(blue.organization); // 还是DaimlerChrysler，Jeep上已经有organization，被blue继承了，所以不会去原型链上找我新定义的organization，但是像color本来没有，所以blue回去prototype上找
Object.keys(blue) == [ 'organizetion' ];
```
![result](https://img-blog.csdnimg.cn/20190212150451422.PNG)
```
// 我也不知道为为什么，这里没有prototype。可能是没有new
// js一切皆为对象，任何对象都有__proto__ 属性
var object = {numProp: 1, stringProp: "foo", obj1Prop: {prop:'foo'}};
console.log(object);
console.log(object.prototype);
console.log(object.__proto__);
console.log(typeof(object));

object.__proto__ = { stringProp: "bar", obj1Prop: {prop: 'bar'}, obj2Prop: {}};
console.log(object);
console.log(object.prototype);
console.log(object.__proto__);

// still be obj1Prop: {prop: 'bar'}
object.obj1Prop.prop = "prop2";
console.log(object.__proto__);

// this will be obj2Prop: {prop: 'prop2'}
object.obj2Prop.prop = "prop2";
console.log(object.__proto__);

// I don't know why obj1Prop and obj2Prop are different

// 结果
// { numProp: 1, stringProp: 'foo', obj1Prop: { prop: 'foo' } }
// undefined
// {}
// object

//{ numProp: 1, stringProp: 'foo', obj1Prop: { prop: 'foo' } }
// undefined
// { stringProp: 'bar', obj1Prop: { prop: 'bar' }, obj2Prop: {} }
// { stringProp: 'bar', obj1Prop: { prop: 'bar' }, obj2Prop: {} }
//{ stringProp: 'bar',
  obj1Prop: { prop: 'bar' },
  obj2Prop: { prop: 'prop2' } }
```
## Closure Mystery
>[闭包](https://segmentfault.me/2016/11/17/%E5%87%BD%E6%95%B0%E4%BD%9C%E4%B8%BA%E8%BF%94%E5%9B%9E%E5%80%BC-%E9%97%AD%E5%8C%85/)
```
var globalVar = 1;
function localFunc(argVar) {
    var localVar = 0;
    function embedFunc() { return ++localVar + ++argVar + ++globalVar; }
    return embedFunc;
}
var myFunc = localFunc(10); // What happens if a call myFunc()? Again?
console.log(myFunc()); // 14 // argVar传进去是多少就是多少
console.log(myFunc());  // 17 因为call了两次myFunc，共用同一个localVar，所以被记住了. argVar也会被记住
console.log(globalVar); // 3 globalVar 对象会变的

var myFunc2 = localFunc(8);
console.log(myFunc2()); // 14（1+9+4） myFunc2()的localVar从0开始计算，因为重新call了localFunc()，myFunc2()的localVar和myFunc()的无关
```
```
console.log(a); // log1 _ _
var a = 3;
function foo(x) {
    console.log(x); // log2 _ _
    var c = 10;
    x = 20;
    console.log(a); // log3 _ _
    a = 4;
    return func;
    function func(d) {
        c = d;
        x *= 2;
        return { a: a, c: c, x: x };
    }
}
console.log(a); // log4 _ _
var bar = foo(a); // 其实此时才会输出 log2, log3
console.log(a); // log5   4，运行closure以后，参数出来就变了
var retVal = bar(3);
console.log(retVal.a); // log6 _ _
retVal = bar(5);
console.log(retVal.c); // log7 _ _
console.log(retVal.x); // log8  80 每一次call bar()就会x*2
console.log(a); // log9 _ _
console.log(retVal.func); // log10 _ _
```
## 匿名函数Mystery
```
var x = 1;
(function (x) {
console.log(x); // 2
x = 3;
})(2);
console.log(x); // 1
```

# Web Application (AngularJS)
## Model, View, Controller（3 tiers）
- Model: stores and manages application data
	- model often gets stored to Angular's scope variables/properties
- View: Defines what the applciation looks like
	- CSS, HTML, Angular Directive, Animations
- Controller: fetches models and control view, handle user interactions
	- Appear as Angular controllers, tied to templates with ng-controller directive to form a component, has angular services, handles events, etc

AngularJS contains a number of concepts including **templates**, **controllers**, **scopes**, **directives**, and **services**.
- ``Angular Directive``: what we use in the HTML to control the behavior
	- isolated, reusable 
- [``Angular Service``:](http://www.runoob.com/angularjs/angularjs-services.html)  **A way of packaging functionality to make it available to any view;** AngularJS constantly supervises your application, and for it to handle changes and events properly, AngularJS prefers that you use the $location service instead of the window.location object.
- **Scopre**: Context where the model data is stored so that templates and controllers can access
	- Scope **digest** and **watches**: 
Two-way binding works by watching when expressions in view template; change and updating the corresponding part of the DOM.
	- Angular add a watch for every variable or function in template expressions
	- During the digest processing all watched expressions are compared to their previously known value and if different the template is reprocessed and the DOM update 
- **Data Binding:** Syncing of the data between the Scope and the HTML (two ways)(View and Model)

## WebApp 的一些特性:
- neea good disign: 
	- consistent, provide context, fast
	- Style guides & design templates
	- use material design
- Deep linking support - AngularJS ``ngRoute``
	- To support bookmarking and sharing we can use ``ngRoute`` to load the views 
	- user to use URLs to directly access context in inside of the application without having to navigate inside
the application
	- I. Intercept the links so that the browser doesn’t handle them
	II. they take advantage of parts of the url that don’t perform full page reloads (i.e. fragments).
- Responsive Support: 
	- To front-end developers response means web application adjusted itself based on the device characteristics.
	- use **breakpoint** in CSS/uses media queries/ (based on screen sizes of popular devices)
```
    @media only screen and (min-width: 768px) {
    /* tablets and desktop layout */ }
    @media only screen and (max-width: 767px) {
    /* phones */ }
    @media only screen and (max-width: 767px) and (orientation: portrait) {
    /* portrait phones */ }
```
- Accessible Rich Internet Applications
	- Add text descriptions for things that need it
``<a aria-label="Photo of user {{user.name}}" ng-href=...`` 
- Internationalization
	- Ultimately need a level of indirection. 
	- language or cultural specific things are parameters to the template rather than hard coded in the template(expect more model components .)

## Single Page Application
- SPA Fetch a page to start, start a JavaScript environment, and then **not** tear the environment down
until the web application finishes.
- Bookmarks the current page, copies the URL for saving or sharing, or pushes the refresh button on the browser. A web application might update the location continuously so to be ready if the user does any of the above events.(we need deep linking)
- **Deep linking**: the URL should capture the web app's context so that directing the browser to the URL will result the app's execution to that context(○Bookmarks ○ Sharing)
	- Maintain the app's context state in the URL
	- Provide a share button to generate deep linking URL
	- ``ngRoute`` - provides routing and deep linking
> Navigating away from the web application or pushing the refresh button will cause the JavaScript execution to terminate, losing any web app state stored in JavaScript (e.g. where in the application the user is, what the user is doing, etc.) One solution for this is to store enough the web application state in the URL so that lost state can be restored. **Deep linking** is a name that is giving for this.

## Testing the web app
- Unit testing
	- Each test targets a particular component and verifies it does what it claims it does
	- Requires mock components for the pieces that component interacts with
	- Example: Load an angular component (controller, directive, etc.) and run tests against it (Need to mock everything these touch (DOM, angular services, etc.))
- End-to-End (e2e) testing
	- Run tests against the real web application
	- Scripting interface into browser used to drive web application
	- Example: Fire up app in a browser and programmatically interact with it. (WebDriver interface in browsers useful for this)
- Metric: Test Coverage(100% test coverage doesn't mean 100% tested(e.g. input)). Increase test case to increase coverage

```
cs142App.controller(’FirstController’, [’$scope’, function ($scope) {
    $scope.first = {};// Need to be initialized before setting $scope.first.<prop>
    $scope.first.greetingIdx = 1; // can be any value
}]);
cs142App.controller(’SecondController’, [’$scope’, function ($scope) {
    $scope.greetings = [’Hello’, ’Hola’];
    $scope.first.selectedGreeting = $scope.greetings[$scope.first.greetingIdx - 1]; 
    // can also initialize in FirstController, and can be any value
    $scope.displayGreeting = function (strIdx) {
        var idx = parseInt(strIdx); // strIdx also works
        if (idx - 1 < $scope.greetings.length) {
            $scope.first.selectedGreeting = $scope.greetings[idx - 1];
        } else {
            $scope.first.selectedGreeting = ""
        }
    }
}]);
```

# ReactJS
- JavaScript framework for writing the web applications
- Uses Model-View-Controller pattern
	- HTML templating approach with **one-way** binding
- Minimal server-side support dictated
- Focus on supporting for programming in the large and single page applications
	- Modules, reusable components, testing, etc.

## Toolchain
- Babel - Transpile language features (e.g. ECMAScript, JSX) to basic JavaScript
- Webpack - Bundle modules and resources (CSS, images); Output loadable with single script tag in any browser

## 组成
- reactApp.js 
	- Render element into browser DOM
- ReactAppView.js
	- **constructor:** set to the attributes passed to the component. set component state(**this.state**) a default value
	- **render():** returns React element tree of the Component's view; Use **JSX** to generate calls to createElement(JSX makes building tree look like templated HTML embedded in JavaScript.)

## One way binding
- JSX statement: ``<input type="text" value={this.state.yourName} onChange={(event) => this.handleChange(event)} />`` Triggers handleChange call with event.target.value == "D"
- handleChange - this.setState({yourName: event.target.value});
this.state.yourName is changed to "D"
- **React sees state change and calls render again** (Feature of React - highly efficient re-rendering)

**compare one-way binding and two-way binding**
[参考](https://stackoverflow.com/questions/34519889/can-anyone-explain-the-difference-between-reacts-one-way-data-binding-and-angula)
- AngularJS: Changes from the code and changes from the HTML are two-way binding. Because of ``ng-model`` setting up watches, change in \<input/> are reflected in $scope. 
- ReactJS: React doesn't have a mechanism to allow the HTML to change the component. The HTML can only raise events that the component responds to. The typical example is by using ``onChange``. The value of the \<input /> is controlled entirely by the render function. The only way to update this value is from the component itself, which is done by attaching an onChange event to the <input /> which sets this.state.value to with the React component method setState. The <input /> does not have direct access to the components state, and so it cannot make changes. This is one-way binding. 

## JSX Programming
- JavaScript calls to React.createElement(type, props, ...children);
- JSX templates must return a valid children parameter when evaluated(no if or for...)(can use JS Ternary operator, JS variables, array for iteration, arrow functions)
- Must use className for HTML class attribute (JS keyword conflict)

## Deep linking support - React Route
To support bookmarking and sharing we can use React Route to load the views
The content div can be the React Route Switch
```
<Switch>
	<Route path="/users/:userId" component={UserDetail} />
	<Route path="/photos/:userId" component={UserPhotos} />
	<Route path="/users" component={UserList} />
</Switch>
```
The UserList sidebar can just use links to view
```
<Link to="/photos/57231f1a30e4351f4e9f4bd8">
	Photos of User Ellen Ripley
</Link>
```
```
import React from 'react';
class ReactAppView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {yourName: ""};
    }
    handleChange(event) {
        this.setState({ yourName: event.target.value });
    }
    render() {
        let label = React.createElement('label', null, 'Name: ');
        let input = React.createElement('input',
            {
                type: 'text', value: this.state.yourName,
                onChange: (event) => this.handleChange(event)
            });
        let h1 = React.createElement('h1', null,
            'Hello ', this.state.yourName, '!');
        return React.createElement('div', null, label, input, h1);
    } // 或者直接ruturn一个树状结构
}
```


