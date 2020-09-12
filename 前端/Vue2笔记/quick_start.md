# 安装环境

- 安装 Vue

 ```
# npm 推荐大型应用使用
sudo apt-get install npm
npm install vue
(npm 要用 node 的，node 也得安装)

# cdn
# study
<!-- 开发环境版本，包含了有帮助的命令行警告 -->
<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>

# production
<!-- 生产环境版本，优化了尺寸和速度 -->
<script src="https://cdn.jsdelivr.net/npm/vue@2.6.11"></script>

# ES Module
<script type="module">
  import Vue from 'https://cdn.jsdelivr.net/npm/vue@2.6.11/dist/vue.esm.browser.js'
</script>
 ```

- 安装 vue-cli 脚手架构建工具

```bash
npm install vue-cli -g

# 新建空的项目文件加并执行
vue init webpack first-vue

cd first-vue
npm install 
npm run dev
```

# 构建版本介绍

- 完整版：包含编译器和运行时（生产环境）
- 编译器：用来将**模板字符串**编译成为 JavaScript 渲染函数的代码
  - `*.vue` 文件内部的模板会在构建时预编译成 JavaScript
- 运行时：用来创建 Vue 实例、渲染并处理虚拟 DOM 等的代码。基本上就是除去编译器的其它一切。（生产环境，且更小）

```bash
npm run dev		# 让项目跑起来
npm run build	# 打包，生成dist文件夹
```

# Hello World

- 简单的嵌在 html 内的 Vue 实例

``helloworld.html``

```html

<html>
<div id="app">
    {{ message }}		
</div>

</html>

<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
<script>
    var app = new Vue({
        el: '#app',
        data: {
            message: 'Hello Vue!'
        }
    })
</script>
```

完整的 Vue 应用

``index.html``

``hello.vue``