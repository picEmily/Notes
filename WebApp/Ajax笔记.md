# Why Ajax
如果仔细观察一个Form的提交，你就会发现，一旦用户点击“Submit”按钮，表单开始提交，浏览器就会刷新页面，然后在新页面里告诉你操作是成功了还是失败了。如果不幸由于网络太慢或者其他原因，就会得到一个404页面。

这就是Web的运作原理：一次HTTP请求对应一个页面。
如果要让用户**留在当前页面中，同时发出新的HTTP请求**，就必须用JavaScript发送这个新请求，接收到数据后，再用JavaScript更新页面，这样一来，用户就感觉自己仍然停留在当前页面，但是数据却可以不断地更新。

# What is Ajax
- **Asynchronous JavaScript and XML**
- AJAX 不是新的编程语言，而是一种使用现有标准的新方法。
- AJAX 是与服务器交换数据并更新部分网页的艺术，在**不重新加载整个页面**的情况下

# How to use Ajax
- AJAX请求是**异步执行**的，也就是说，要通过**回调函数**获得响应。
- 在现代浏览器上写AJAX主要依靠``XMLHttpRequest``对象：

## 发送请求
- ``open(method,url,async)``
	- 规定请求的类型、URL 以及是否异步处理请求。
	- method：请求的类型；GET 或 POST
	- url：文件在服务器上的位置
	- async：true（异步）或 false（同步）
- send(string)
	- GET 请求没参数
	- string：仅用于 POST 请求

## 处理相应

最基本写法（不支持ie）
```javascript
function success(text) {
    var textarea = document.getElementById('test-response-text');
    textarea.value = text;
}

function fail(code) {
    var textarea = document.getElementById('test-response-text');
    textarea.value = 'Error code: ' + code;
}

var request = new XMLHttpRequest(); // 新建XMLHttpRequest对象

request.onreadystatechange = function () { // 状态发生变化时，函数被回调
    if (request.readyState === 4) { // 成功完成
        // 判断响应结果:
        if (request.status === 200) {
            // 成功，通过responseText拿到响应的文本:
            return success(request.responseText);
        } else {
            // 失败，根据响应码判断失败原因:
            return fail(request.status);
        }
    } else {
        // HTTP请求还在继续...
    }
}

// 发送请求:
request.open('GET', '/api/categories');
request.send();

alert('请求已发送，请等待响应...');
```

# Jquery 库中的 Ajax
Jquery通过$.get, $.post，$.ajax() 返回其创建的 XMLHttpRequest 对象

例子：Jquery+Ajax上传文件
https://mkyong.com/jquery/jquery-ajax-submit-a-multipart-form/

只写了前端，通过api("/api/upload")请求来upload文件。后端只需要提供api就好了。
```html
{% block js %}
<script type="text/javascript">
    $(document).ready(function () {
        $("#btn_upload").click(function (event) {
            event.preventDefault();
            var form_data = new FormData($('#fileUploadForm')[0])

            $.ajax({
                type: 'POST',
                url: '/api/upload',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
                success: function (response) {
                    if (response != 0) {
                        alert('file uploaded');
                    }
                    else {
                        alert('file not uploaded');
                    }
                },
            });
        });
    }); 
</script>
{% endblock %}

{% block body %}
<p id="post{{ post.id }}"> {{ post.body }} </p>
<h2>Upload your resume</h2>
<form method="post" enctype="multipart/form-data" , id="fileUploadForm">
    <input type="file" name="file" id="file">
    <input type="submit" value="Upload" id="btn_upload">
</form>
{% endblock %}
```