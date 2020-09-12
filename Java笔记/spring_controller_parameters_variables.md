# SpringMVC Controller 接收参数的注解

``@PathVariable``: URL中绑定的占位符

``@RequestParam``: URL中 ?xxx=xxx这些

``@RequestBody``: 把参数丢到body里面

和 get post 无关



## 上传file的时候

controller 用 @RequestParam 来接收 （？？？为啥）

file 放在form data里，content-type 要设置为 multipart/formdata

传递的数据是binary格式（乐意的话也能用blob，但我没研究）