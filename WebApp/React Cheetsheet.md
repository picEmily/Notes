# React Cheetsheet
**比较好的资料**
- MDN
- React文档
- 微软React bootcamp

**练习**
- todo list 如图所示
![](https://i.imgur.com/YulLt1m.png)

**目录**
- HTML 和 CSS
	- CSS选择器
	- DOM
- JS
	- variables
	- functions (特殊：箭头函数，callback)
	- operators
	- events
	- control flow
	- interacting with the DOM
	- export and import
	- 其他一些需要注意的点
- React哲学 High Level： https://reactjs.org/docs/thinking-in-react.html
- React基本构成（静态版本，不含交互功能）
	- JSX
	- 组件 component
	- state，props
- 动态UI（传递state）
	- 从上往下传递
	- 从下往上传递
	- types
- UI Fabric component library
- 复杂的app数据传递
	- context api
	- redux框架

# HTML 和 CSS
## HTML 略
## CSS选择器
![](https://raw.githubusercontent.com/Microsoft/frontend-bootcamp/master/assets/css-syntax.png)

## DOM
https://developer.mozilla.org/zh-CN/docs/Web/API/Document_Object_Model/Introduction
- DOM是把document解析成节点和对象的集合（document指的是html，xml文档）
- 通过脚本语言（JS，PYTHON）可以与DOM交互（改变文档）

# JS
## variable
boolean: ``true, false``
number: ``1``, ``3.14``
string: ``'single quotes'``, ``"double quotes"``, or ```backticks```
array: ``[ 1, 2, 3, 'hello', 'world']``
object: ``{ foo: 3, bar: 'hello' }``
function: ``function(foo) { return foo + 1 }``
``null``
``undefined``

**let, var, const 的区别**

## functions
### 普通
```
function displayMatches() {
  alert("I'm Clicked");
}
```

### 箭头函数
箭头函数表达式的语法比函数表达式**更简洁**，并且没有自己的``this``，``arguments``，``super``或``new.target``。箭头函数表达式更适用于那些本来需要匿名函数的地方，并且它不能用作构造函数。

```javascript
// 一般情况 
(param1, param2, …, paramN) => { statements } 
(param1, param2, …, paramN) => expression
//相当于：(param1, param2, …, paramN) =>{ return expression; }

// 当只有一个参数时，圆括号是可选的：
(singleParam) => { statements }
singleParam => { statements }

// 没有参数的函数应该写成一对圆括号。
() => { statements }
```
各种细节：https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Functions/Arrow_functions

### callback
TODO

### 常用内置函数
``filter``: 对一个数组进行过滤，返回一个新数组
https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Array/filter
```javascript
var newArray = arr.filter(
	callback(element[, index[, array]])
	[, thisArg]
)

// e.g.
function fn(element) {
	return element > 10; 
}

var unfiltered = [1,3,10,30];
var filtered = unfiltered.filter(fn);
console.log(unfiltered); // 不改变原数组[1,3,10,30]
console.log(filtered); // [30]
```
只有element参数是必须的

``map``: 创建一个新数组，其结果是该数组中的每个元素都调用一个提供的函数后返回的结果。
``callback`` 函数会被自动传入三个参数：数组元素，元素索引，原数组本身。
```javascript
var new_array = arr.map(
	function callback(currentValue[, index[, array]]) {
 		// Return element for new_array 
	}
	[, thisArg])

//  e.g. 1
// roots的值为[1, 2, 3], numbers的值仍为[1, 4, 9]
var numbers = [1, 4, 9];
var roots = numbers.map(Math.sqrt);

// 也可指定参数，这个参数会自动被分配成数组中对应的每个元素
var numbers = [1, 4, 9];
var doubles = numbers.map(function(num) {
  return Math.sqrt(num);
});

// e.g.2
// 最一般性的方法
var a = Array.prototype.map.call("Hello World", function(x) { 
  return x.charCodeAt(0); 
})
// a的值为[72, 101, 108, 108, 111, 32, 87, 111, 114, 108, 100]
```

## operators
**ternary operator** ``condition ? expressionIfTrue : expressionIfFalse``


``...``: spread operate **扩展运算符**
对象中的扩展运算符(...)用于取出参数对象中的所有可遍历属性，拷贝到当前对象之中
```javascript
let bar = { a: 1, b: 2 };
let baz = { ...bar }; // { a: 1, b: 2 }
```


``==`` and ``===``

## events
让函数可以作用到页面上，函数需要依附events。总体而言包括鼠标，键盘，文档加载。有好几种方法可以绑定event和函数。

```javascript
// event listener
window.addEventListener('load', function() {
  console.log('loaded');
});

// event handler
window.onload = function() {
  console.log('loaded!');
};

// trigger function when button is clicked
document.querySelector('.submit').onclick = displayMatches;
```

## control flow
```javascript
for (foo of foos) {
	// ...
}
```

## interacting with the DOM
我们可以用``document.querySelector``

```javascript
const submit = document.querySelector('.submit');
```

## module
ES6规范（浏览器环境）: import and export
ES6中需要先export了才能import
```javascript
export class Counter extends React.Component {
  // ...
}

import { Counter } from './components/Counter';
```

另有commonjs规范用于node.js环境（后端）

## JS的异步（说实话我还是不太理解）
https://developer.mozilla.org/zh-CN/docs/learn/JavaScript/%E5%BC%82%E6%AD%A5/%E6%A6%82%E5%BF%B5

https://developer.mozilla.org/zh-CN/docs/learn/JavaScript/%E5%BC%82%E6%AD%A5/%E7%AE%80%E4%BB%8B

Javascript语言的执行环境是"单线程"（single thread）
但是有时候某个任务特别耗时间，或者某个代码是阻塞代码(例如``alert()``)，我们不希望其阻塞之后的任务
- 老派的解决方法是callback
- 新派的解决办法是promise

## promise
https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Guide/Using_promises

中文参考：
https://www.jianshu.com/p/b16e7c9e1f9f

- A promise is an **object** representing work that will be completed later, **asynchronously**. 
- Promises are **chainable**, which helps with writing maintainable async code. 
	- Typically, legacy async code uses **callbacks** to let the caller have control over what to do after the task has been completed, which becomes very hard to read.)
	- 链式操作的最大好处就是避免了回调地狱
	- 本质上，Promise 是一个被某些函数传出的对象，**我们附加回调函数（callback）使用它，而不是将回调函数传入那些函数内部。**

```javascript
// promise 对象
var promise = new Promise(function(resolve, reject){
    // ... some code
    
    if (/* 异步操作成功 */) {
        resolve();
    } else {
        reject();
    }
});

// 返回一个 promise 对象，回调函数绑定在该 Promise 上
// then
promise.then(() => console.log("finished"), () => console.log("failed"));
```
promise
- 接收一个函数作为参数，该函数接收``resolve``,``reject``两个函数作为参数
-  resolve作用是将Promise对象状态由“未完成”变为“成功”，也就是Pending -> Fulfilled，在异步操作成功时调用，并将异步操作的结果作为参数传递出去；
-  reject函数则是将Promise对象状态由“未完成”变为“失败”，也就是Pending -> Rejected，在异步操作失败时调用，并将异步操作的结果作为参数传递出去。

then
- Promise实例生成后，可用then方法分别指定两种状态回调参数。then 方法可以接受两个回调函数作为参数：
- Promise对象状态改为Resolved时调用 （必选）
- Promise对象状态改为Rejected时调用 （可选）

例子：执行顺序
```javascript
let promise = new Promise(function(resolve, reject){
    console.log("AAA");
    resolve()
});
promise.then(() => console.log("BBB"));
console.log("CCC")

// AAA
// CCC
// BBB
```
执行后，我们发现输出顺序总是 AAA -> CCC -> BBB。表明，**在Promise新建后会立即执行**，所以首先输出 AAA。然后，**then方法指定的回调函数将在当前脚本所有同步任务执行完后才会执行**，所以BBB 最后输出。


## Async / await
https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Statements/async_function

写的比文档好：
https://segmentfault.com/a/1190000007535316

- Async / Await is a language-level feature for writing **asynchronous functions as if they are ordinary, synchronous code**
- **异步函数是指通过事件循环异步执行的函数，它会通过一个隐式的 ``Promise`` 返回其结果。**
	- 如果在函数中 return 一个直接量，async 会把这个直接量通过 ``Promise.resolve()`` 封装成 ``Promise`` 对象。
- 异步函数可以包含``await``指令，该指令会**暂停异步函数**的执行，并**等待Promise执行**，**然后继续执行异步函数**，并返回结果。
	- ``await`` 关键字只在**异步函数内**有效。如果你在异步函数外使用它，会抛出语法错误。
- ``async/await``的**目的是**简化使用多个 ``promise`` 时的同步行为，并对一组 ``Promises``执行某些操作。正如Promises类似于结构化回调，``async/await``更像结合了``generators``和 ``promises``。


```javascript
async function someFunctionAsync() {
  // Inside here, we can await on other async functions
  const result = await someOtherFunctionAsync();
  return result + ' hello'; // 隐式返回promise对象的结果
}

// 这个result参数从哪传进来？
someFunctionAsync().then(result => {
  console.log(result);
});
```
- ``async`` 函数必定返回 ``Promise``，我们把所有返回 ``Promise`` 的函数都可以认为是异步函数
- ``await``命令后面是一个 ``Promise`` 对象，返回该对象的结果。如果不是 ``Promise`` 对象，就直接返回对应的值。


# React 哲学（React app 构建步骤）
https://zh-hans.reactjs.org/docs/thinking-in-react.html
1. 将设计好的UI划分为组件层级
2. 用 React 创建一个静态版本
	- 不包含交互功能的UI
	- 通过props传递数据，**不要**使用state
	- 自上而下或自下而上构建应用
	- ``ReactDOM.render()``渲染
3. 确定 UI state 的最小（且完整）表示
	- 确定我们需要哪些state
	- 只用最少的state，其他数据均由它们计算产生
4. 确定 state 放置的位置
	- **React数据流是单向的，并顺着组件层级从上往下传递**
	- 找到使用该state并且层级最高的组件存放state
	- 在constructor中给state赋予初值
	- 通过props把state传递下去给其他组件
5. 添加反向数据流
	- 较低层级的组件更新较高层级组件的state（但是React只允许拥有state的组件更改该state）
	- 高级组件传递一个能够触发state改变的callback传递给低级组件
	- 结合事件监听(e.g. ``onChange()``)和``setState()``

> AngularJS是双向绑定，React是单向绑定。
> 具体的区别：TODO

# React基本构成
## JSX
https://reactjs.org/docs/introducing-jsx.html
- 是JS的补充(syntax extension of JavaScript)
- 在React中使用，用来产生React elements

我们在前端中需要关注的是**UI logic**
- how events are handled
- how the state changes over time
- how the data is prepared for display

React通过**Components**将markup(html)和逻辑结合在一起（即view和controller结合起来）

### JSX使用注意事项
https://www.runoob.com/react/react-jsx.html
- 在 JSX 中不能使用 ``if else`` 语句，但可以使用 三元运算表达式来替代。
- ``{/*注释...*/}``
- 在 JSX 中使用 JavaScript 表达式。表达式写在花括号 {} 中。


## ReachDOM.render()
更新UI界面的方法
React和DOM的交互
注意``render()``只能返回一个element
```javascripts
ReactDOM.render(content, place);
```

## React Component（组件）
https://react.docschina.org/docs/components-and-props.html
- 前面讲到过React由一个一个component组成
- **A React component is a piece of code that returns a portion of your application.** 
	- This can include HTML markup, CSS styles, and JavaScript driven functionality.
- 两种方法
	- JavaScript class
	- function

```JavaScript
// 方法1：继承React.Component
class App extends React.Component {
  render() {
    return <p>Hello World</p>;
  }
}

// 方法2：App是一个函数
const App = props => {
  // 参数是props
  return <p>Hello World</p>;
};

function App(props) {
  return <h1>Hello World</h1>;
}
```

**e.g. 时钟**
https://react.docschina.org/docs/state-and-lifecycle.html
- 完整的通过class实现component
包括构造函数，``render()``，state，props
- 实现生命周期

```JavaScript
class Clock extends React.Component {
  constructor(props) {
    super(props);
    this.state = {date: new Date()};
  }

  componentDidMount() {
    this.timerID = setInterval(
      () => this.tick(),
      1000
    );
  }

  componentWillUnmount() {
    clearInterval(this.timerID);
  }

  tick() {
    this.setState({
      date: new Date()
    });
  }

  render() {
    return (
      <div>
        <h1>Hello, world!</h1>
        <h2>It is {this.state.date.toLocaleTimeString()}.</h2>
      </div>
    );
  }
}

ReactDOM.render(
  <Clock />,
  document.getElementById('root')
);

```

## props，state
https://zh-hans.reactjs.org/docs/faq-state.html#what-is-the-difference-between-state-and-props
- props是组件的属性，是一个存储数据的对象，props的特点是**不会被更改**
- state也是存储数据的，但是其为组件私有，**可以在class中被修改**
	- 在class中使用，在构造函数中赋予初值，且构造函数是唯一可以给 ``this.state`` 赋值的地方
	- state要通过工厂方法修改``setState()``

**数据的向下流动**
除了拥有并设置了state的组件，其他组件都无法访问。
组件可以选择把它的 state 作为 props 向下传递到它的子组件中

> 将函数作为参数的意义：
state的更新可能是异步的，不能依赖其值来更新下一个状态，所以可以接收函数作为对象，这样一来一定会使得依赖的函数先执行：

```javascript
// 当state属于这个class，这样是对的
// 当state继承自其父组件，这样不对
this.setState({
  counter: this.state.counter + this.props.increment,
});

// // 当state继承自其父组件，这样对
this.setState((state, props) => ({
  counter: state.counter + props.increment
}));
```

# 动态UI
## 从上往下传递
```javascript
// 父组件中通过constructor给state赋值
class ParentComponent extends React.Component {
	constructor(props) {
	  super(props);
	  this.state = foo;
	}
	
	render() {
		//...
		return ...
	}
}


// 子组件中接收到state
class SonComponent extends React.Component {
	render() {
	  const bar = this.state;
	  return (
	  	<div bar={bar} />
	  );
	}
}
```

## 从下往上传递
- 所谓从下往上传递就是低级组件能够改变state的值并传递给高级组件。
- 根据React的规则，React是单向传递的，无法直接从下往上传递。即只有拥有state的组件才能直接改变该state。
- 需要通过callback function完成。

**e.g. ``<input />``**
```javascript
// Parent Component constructor
this.state = { labelInput : '' };

// Parent Component defines the callback fn
_onChange = evt => {
  this.setState({ labelInput: evt.target.value });
};

// Son Component get the callback fn
render() {
	// ...
	return
		<input value={this.state.labelInput} onChange={this._onChange} className="textfield" placeholder="add sth" />
}
```

## types
定义某个component的props的types
Component可以继承这个interface
```javascript
// interface
interface TodoListProps {
  filter: 'all' | 'active' | 'completed'; // 只能从这三个字符串里选一个
  todos: { 
	// 复杂对象
    [id: string]: {
      label: string;
      completed: boolean;
    };
  }; 
  complete: (id: string) => void; // 函数
}

// component 继承
// Note that the first value in <> is for a props interface, and the second is for state.
export class TodoList extends React.Component<TodoListProps, any>
```

# UI Fabric component library
文档
https://developer.microsoft.com/en-us/fabric/#/controls/web/button

stack文档
https://developer.microsoft.com/en-us/fabric#/controls/web/stack

- 微软提供的一些官方的设计，简化我们自己设计
- 值得注意的是flexbox在Fabric里面被抽象成``stack``对象，简化了flexbox的使用
- 可以使用主题 https://github.com/hzwdachui/frontend-bootcamp/tree/master/step2-03/demo

例子
```javascript
// button
import { DefaultButton } from 'office-ui-fabric-react';
const MyComponent = () => {
  return (
    <div>
      <DefaultButton iconProps={{ iconName: 'Mail' }}>Send Mail</DefaultButton>
    </div>
  );
};

// stack
import { Stack } from 'office-ui-fabric-react';
// <Stack> </Stack>
// <StackItem> </StackItem>

// theme
<Customizer {...FluentCustomizations}> </Customizer>
```

# 复杂app的数据传递
- Data needs to be passed down from component to component via props--even if some of the intermediate components don't need to know about some of the data. This is a problem called props drilling.
- Shared data can be changed by various actors (user interaction, updates from server), and there is no coordination of these changes. This makes propagating updates between components challenging.

需要用到：
- Context API：把props，state的传递包装一下，看起来没那么繁琐
- Redux library：React中数据存储的中心(store)

## context api
```javascript
// parent
<TodoContext.Provider
  value={{
    ...this.state,
    addTodo: this._addTodo,
    setFilter: this._setFilter,
    /* same goes for remove, complete, and clear */
  }}>
</TodoContext.Provider>

// consumer1
class TodoHeader extends React.Component {
  render() {
    // Step 1: use the context prop
    return <div>Filter is {this.context.filter}</div>;
  }
}

// Step 2: be sure to set the contextType property of the component class
TodoHeader.contextType = TodoContext;

// consumer2
const TodoFooter = props => {
  const context = useContext(TodoContext);
  return (
    <div>
      <button onClick={context.clear()}>Clear Completed</button>
    </div>
  );
};
```

## Redux （说实话没太明白）
中文第三方文档
http://cn.redux.js.org/

- 适合中大型应用
- 我个人理解是提供给React的一个框架，规范化data传递的流程
- 与Redux对应，原来传统的方式称为Flux

![](https://i.imgur.com/bfZS330.png)

### Redux的各个部分
- view：React中的组件(component)，从store中获取数据
- action：JSON，传递event，可以影响state
- store
	- dispatcher：获取action，传递给reducer
	- reducer：获取state tree和action，更新state tree（唯一更新state tree的方法）
	- state tree：singleton, serializable, immutable nested JSON structure. 通过reducer更新

### store的写法
```javascript
// create store
const store = createStore(reducer, initialState);

// reducers
import { createReducer } from 'redux-starter-kit';
import { combineReducers } from 'redux';
// creatReducer 创建各个子reducer
// combineReducer 把reducer组合起来

// actions
export const actions = {
  addTodo: (label: string) => ({ type: 'addTodo', id: nextId(), label }),
  remove: (id: string) => ({ type: 'remove', id }),
  complete: (id: string) => ({ type: 'complete', id }),
  clear: () => ({ type: 'clear' }),
  setFilter: (filter: string) => ({ type: 'setFilter', filter })
};

// dispatch
const action = actions.addTodo('foo');
store.dispatch(action);
store.dispatch(actions.complete(action.id));
```

### 结合redux和react
redux只解决了数据传递，我们还要把数据渲染到app中
- ``<Provider store={store}> </Provider>``
- mapping: ``connec()``函数

```javascript
import { connect } from 'react-redux';

const MyComponent = props => {
	// 假设我有这个一个component
  return <div>
    {props.prop1}
    <button onClick={props.action1()}>Click Me</button>
  </div>;
};

const ConnectedComponent = connect(
  state => {
    prop1: state.key1,
    prop2: state.key2
  },
  dispatch => {
    action1: (arg) => dispatch(actions.action1(arg)),
    action2: (arg) => dispatch(actions.action2(arg)),
  }
)(MyComponent);
```
- 参数
	- Redux state tree
	- dispatch functions
- 返回值：一个函数，这个函数以``MyComponent``为参数