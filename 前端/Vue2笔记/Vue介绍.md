# 基本认识

- 渐进式框架：由底向上逐层构建应用
- 可复用的组件
- 非侵入
- 响应式：（Reactive）当一个数据变更，所有用到它的地方都响应

# 语法

- 模板语法
- 渲染函数 JSX

## 模板语法

- 插值：``{{  }}``
- 指令：``v-``
  - 指令 (Directives) 是带有 `v-` 前缀的特殊 attribute。
  - 当表达式的值改变时，将其产生的连带影响，响应式地作用于 DOM。

### 指令

- ``v-bind``: 响应式更新 attribute

  ```html
  <!-- 完整语法 -->
  <a v-bind:href="url">...</a>
  
  <!-- 缩写 -->
  <a :href="url">...</a>
  
  <!-- 动态参数的缩写 (2.6.0+) -->
  <a :[key]="url"> ... </a>
  ```

  

- ``v-on``：监听 DOM 事件

  ```html
  <!-- 完整语法 -->
  <!-- doSonething 是方法的名称 -->
  <a v-on:click="doSomething(args)">...</a>
  
  <!-- 缩写 -->
  <a @click="doSomething">...</a>
  
  <!-- 动态参数的缩写 (2.6.0+) -->
  <a @[event]="doSomething"> ... </a>
  ```

  ```html
  - 原始 DOM 事件
  - 键盘事件/鼠标事件
  
  DOM 事件修饰符
  .stop
  .prevent
  .capture
  .self
  .once
  .passive
  
  键盘事件
  
  鼠标事件
  
  <!-- 阻止单击事件继续传播 -->
  <a v-on:click.stop="doThis"></a>
  
  <!-- 提交事件不再重载页面 -->
  <form v-on:submit.prevent="onSubmit"></form>
  
  <!-- 修饰符可以串联 -->
  <a v-on:click.stop.prevent="doThat"></a>
  
  <!-- 只有修饰符 -->
  <form v-on:submit.prevent></form>
  
  <!-- 添加事件监听器时使用事件捕获模式 -->
  <!-- 即内部元素触发的事件先在此处理，然后才交由内部元素进行处理 -->
  <div v-on:click.capture="doThis">...</div>
  
  <!-- 只当在 event.target 是当前元素自身时触发处理函数 -->
  <!-- 即事件不是从内部元素触发的 -->
  <div v-on:click.self="doThat">...</div>
  
  ```

- ``v-if``, ``v-else``, ``v-else-if``

- ``v-for``

- ``v-model``: 表单输入绑定，**双向绑定**

  - ``<input>``、``<textarea>``、 ``<select>``
  - 修饰符 ``.lazy``, ``.number``, ``.trim``
  
  ```html
  
  ```
  
- 



# 需要计算的内容

- 计算属性
- 方法
- 侦听属性：``watch`` 回调

## 计算属性

- 基于响应式依赖进行缓存，只有依赖发生变化才重新求值 (方法则不是，每次渲染都是重新执行)

```html
<div id="example">
  <p>Original message: "{{ message }}"</p>
  <p>Computed reversed message: "{{ reversedMessage }}"</p>
  <p>Computed reversed message: "{{ reversedMessage() }}"</p>
  <p>Computed reversed message: "{{ fullname }}"</p>
</div>

<script>
var vm = new Vue({
  el: '#example',
  data: {
    message: 'Hello',
    firstname: 'Ming',
    lastname: 'Xiao'
  },
  computed: {
    // 计算属性的 getter，指明的话默认是 getter
    reversedMessage: function () {
      // `this` 指向 vm 实例
      // 这里的依赖是 message
      return this.message.split('').reverse().join('')
    },
    fullname: {
        // 指明 getter 和 setter 方法
        // getter
        get: function () {
            return this.firstname + ' ' + this.lastname
        }
        // setter
        set: function (newValue) {
      		var names = newValue.split(' ')
      		this.firstName = names[0]
      		this.lastName = names[names.length - 1]
  		}
    }
  },
  methods: {
    reversedMessage: function () {
    return this.message.split('').reverse().join('')
  }
})
</script>
```



## 监听属性



# 组件

- 组件的 data 必须是函数