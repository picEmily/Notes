# matplotlib
**入门：**
https://matplotlib.org/3.2.2/tutorials/index.html

**教程：**
https://matplotlib.org/3.2.2/tutorials/introductory/usage.html#sphx-glr-tutorials-introductory-usage-py
1. 导入 ``import``
2. 创建figure画布对象
	- 显式 ``fig = plt.figure()``
	- 隐式 ``plt.plot()``
3. 绘制 ``matplotlib.pyplot``
	- figure: 画布
	- axes：坐标系（图分为几个部分）（画布的子集）
	- axis：坐标轴（每张图上画的线条）
	- artist ？？？

**两种风格**
- OO-style
- pyplot-style

**matplotlib.pyplot**
https://matplotlib.org/3.2.2/tutorials/introductory/pyplot.html#sphx-glr-tutorials-introductory-pyplot-py
```python
# open an image
# https://matplotlib.org/api/_as_gen/matplotlib.pyplot.imread.html
matplotlib.pyplot.imread(fname, format=None)[source]

# show the image
# imshow() draw the image and show() print the image
# https://matplotlib.org/3.2.2/api/_as_gen/matplotlib.pyplot.imshow.html
matplotlib.pyplot.imshow(X, cmap=None, norm=None, aspect=None, interpolation=None, alpha=None, vmin=None, vmax=None, origin=None, extent=None, shape=<deprecated parameter>, filternorm=1, filterrad=4.0, imlim=<deprecated parameter>, resample=None, url=None, *, data=None, **kwargs)[source]
matplotlib.pyplot.show()	
```

# Pillow
document: https://pillow.readthedocs.io/en/stable/
Python中处理图片的库

**Image Module**
```python
# open an image
img = PIL.Image.open(fp, mode='r')

# show the image
img.show()
PIL.ImageShow.show(img, title=None, **options)
```

# HTML中渲染matplotlib图像
将图像储存在变量（内存）中
- 借助IO（``BytesIO``, ``StringIO``...），可以不用保存图片到磁盘然后再读取
- base64 编码：
	- **Base64是网络上最常见的用于传输8Bit字节码的编码方式之一**，Base64就是一种基于64个可打印字符来表示二进制数据的方法。（可以用记事本打开图片了！）
	- 可用于图片编码

```python
import os
import base64

imgdata = io.BytesIO()
fig.savefig(imgdata, format='png')
imgdata.seek(0)  # rewind the data
plot_url = "data:image/png;base64" + base64.b64encode(img.getvalue()).decode()

# <img src="{{ plot_url }}">
```

# 用户上传图片并预览
**需求：**
- 前端实现上传图片并**预览**，同时发送图片数据给后端
- 后端处理图片再返回前端，前端显示处理后的图片

方法一：（略）
-  上传图片，保存到本地 例如``static/uploads``（也可以借助云，减轻服务器压力）
-  再从本地读取图片

方法二：（接下来讨论的方法）
- 前端直接实现预览
- ajax发给后端处理

## 前端部分
``input``**标签**：
- ``type="file"``返回一个``FileList``，无multiple属性时则只有要给对象
- ``multiple``表示能接受多个文件
- ``accept``接受文件的类型
- ``capture``移动端拍照

```javascript
# 1. accept='image/png' 或者 accept='.png' --只接受 .png 格式的图片
# 2. accept='iamge/png,image/jpeg' 或者 accept='.png, .jpg .jpeg' 接受 .png .jpeg .jpg 格式的图片
# 3. accept='image/*' 接受所有类型的 image 

<input type="file" multiple accept="image/*"> 
```

**使用文件**
``FileList``**对象**
https://developer.mozilla.org/zh-CN/docs/Web/API/File/Using_files_from_web_applications

``FileReader``**对象**
https://developer.mozilla.org/zh-CN/docs/Web/API/FileReader
```
FileReader.onload() 
# 处理load事件。该事件在读取操作完成时触发。
# 当 FileReader 读取文件的方式为  readAsArrayBuffer, readAsBinaryString, readAsDataURL 或者 readAsText 的时候，
# 会触发一个 load 事件。
# 从而可以使用  FileReader.onload 属性对该事件进行处理。

FileReader.readAsDataURL() 
# 开始读取指定的Blob中的内容。一旦完成，result属性中将包含一个data: URL格式的Base64字符串以表示所读取文件的内容。
```

**Minimum Sample**: 
https://stackoverflow.com/questions/14069421/show-an-image-preview-before-upload
```javascript
<input type="file" id="files" />
<img id="image" />

document.getElementById("files").onchange = function () {
    var reader = new FileReader();

    reader.onload = function (e) {
        // get loaded data and render thumbnail.
        document.getElementById("image").src = e.target.result;
    };

    // read the image file as a data URL.
    reader.readAsDataURL(this.files[0]);
};
```

其他参考：
https://juejin.im/post/5ad365e4f265da237d0375a5
https://juejin.im/post/5a0545a75188254d2b6d979c

**在图片上实现鼠标标点**
- ``Element.getBoundingClientRect()`` 获取元素位置
- ``MouseEvent.clientX`` ``MouseEvent.clientY`` 获取鼠标指针位置
- ``mousemove``, ``click`` 等鼠标事件
- ``<canvas/>`` 编辑图片：https://segmentfault.com/a/1190000022026418
	- https://developer.mozilla.org/zh-CN/docs/Web/API/Canvas_API/Tutorial/Drawing_shapes

在canvas上绘制，获取canvas的位置
```html
<canvas id="myCanvas"></canvas> # 据我观察会生成一个width:300 height:150的矩形canvas
```

```javascript
function draw() {
  var canvas = document.getElementById('myCanvas');
  if (canvas.getContext) {
	// context
    var ctx = canvas.getContext('2d');
	
	// 在context上绘制图形
    ctx.fillRect(25, 25, 100, 100);
    ctx.clearRect(45, 45, 60, 60);
    ctx.strokeRect(50, 50, 50, 50);

	// 如果是在 canvas上放image
    canvas.width = img.width;
    canvas.height = img.height;
    ctx.drawImage(img, 0, 0);
  }
}

document.getElementById("myCanvas").addEventListener("click", e => {
	// 在canvas上点击鼠标则执行draw()	
	draw();
})

function getPosition() {
	rect = canvas.getBoundingClientRect();
}

// print
for (var key in rect) {
    if(typeof rect[key] !== 'function') {
		// 一共有6个属性
        // x, y, width, height, top, right, bottom, left
        console.log(`${ key } : ${ rect[key] }`);
    }
}
```


获取鼠标位置
```html
<p id="screen-log"></p>
```

```javascript
// 鼠标移动事件=>执行logKey()
document.addEventListener('mousemove', logKey);

function logKey(e) {
    document.querySelector('#screen-log').innerText = `Client X/Y: ${e.clientX}, ${e.clientY}`;
}
```

**ajax发送请求给服务器并接受响应**
文档：
https://developer.mozilla.org/zh-CN/docs/Web/Guide/AJAX
https://api.jquery.com/jQuery.ajax/
https://www.w3school.com.cn/jquery/ajax_ajax.asp
结合jQuery实现简单一点（写法和阅读都简单一些），我就不研究传统方法了
``XMLRttpRequest = new XMLHttpReqest()``对象是核心，提供异步发送请求的能力

Ajax只动态更新**部分**内容，不影响页面中其他操作。
- 异步引擎对象发送请求
- 响应内容只是需要的数据

使用 ``XMLHttpRequest``
https://developer.mozilla.org/zh-CN/docs/Web/API/XMLHttpRequest/Using_XMLHttpRequest#%E6%8F%90%E4%BA%A4%E8%A1%A8%E5%8D%95%E5%92%8C%E4%B8%8A%E4%BC%A0%E6%96%87%E4%BB%B6
https://api.jquery.com/jQuery.ajax/

``jQuery.ajax( [settings] )``例子
```javascript
 $.ajax({
    url: 'http://127.0.0.1:5000/debug/mobius/api/v1/imgUpload',
    type: 'POST',
    data: formFile,
    async: true,  
    cache: false,  
    contentType: false, 
    processData: false, 
    // traditional:true,
    dataType:'json',
    success: callback, 
    error: function() {
		console.log("Error");
	}
});

# FormFile是FormData对象。使用起来和数组差不多
# https://developer.mozilla.org/en-US/docs/Web/API/FormData
var formFile = new FormData();
```
最重要：
- ``type``: 请求的类型
- ``data``: 请求的对象（最好json序列化） 
- ``success``: 一个函数，响应成功时执行
- ``error``: 一个函数，响应失败时执行

其他：
- ``async``: 默认true，异步执行
- 其他的看文档

其他参考：
https://zhuanlan.zhihu.com/p/24429519
https://blog.csdn.net/chenHaiJaheike/article/details/89045939

## 后端部分
**flask 读取 form post requset：**
```
# https://tedboy.github.io/flask/generated/generated/werkzeug.FileStorage.html
request.files['myImg'] # FileStorage 对象

# https://stackoverflow.com/questions/20015550/read-file-data-without-saving-it-in-flask
request.files['myImg'].read() # bytes 对象
io.BytesIO([Bytes_Object]) # 存储bytes对象在IO中

request.form # 返回Immutabledict，是整个请求
json.loads(request.form) # 读取的时候load一下
```








