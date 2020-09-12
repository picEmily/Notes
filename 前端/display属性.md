# display  定义和用法

display 属性规定元素应该生成的框的类型。

主要用来布局。

| 值           | 描述                                                 |
| :----------- | :--------------------------------------------------- |
| none         | 此元素不会被显示。                                   |
| block        | 此元素将显示为块级元素，此元素前后会带有换行符。     |
| inline       | 默认。此元素会被显示为内联元素，元素前后没有换行符。 |
| inline-block | 行内块元素。（CSS2.1 新增的值）                      |
| list-item    | 此元素会作为列表显示。                               |

# Position 定义和用法

position 属性规定元素的定位类型。

绝对或固定元素会生成一个块级框，而不论该元素本身是什么类型。相对定位元素会相对于它在正常流中的默认位置偏移。

| 值       | 描述                                                         |
| :------- | :----------------------------------------------------------- |
| absolute | 生成绝对定位的元素，**相对于 static 定位以外的第一个父元素进行定位**。元素的位置通过 "left", "top", "right" 以及 "bottom" 属性进行规定。 |
| fixed    | 生成绝对定位的元素，相对于**浏览器窗口**进行定位。元素的位置通过 "left", "top", "right" 以及 "bottom" 属性进行规定。 |
| relative | 生成相对定位的元素，相对于其正常位置进行定位。因此，"left:20" 会向元素的 LEFT 位置添加 20 像素。 |
| static   | 默认值。没有定位，元素出现在正常的流中（忽略 top, bottom, left, right 或者 z-index 声明）。 |
| inherit  | 规定应该从父元素继承 position 属性的值。                     |



## 如何让元素居中

- 利用 line-height 设置行间距
- 行间距分为两半，一般加到文本顶部，一半加到文本底部
- 要把 font-size 也计算进去

```html
<html>
<div id="father">
    <div id="son">+</div>
</div>
</html>

<style>
    #father {
        width: 400px;
        height: 400px;
        border: solid black 1px;
        text-align: center;
        line-height: 400px;
    }
    #son {
        display: inline-block;
    }
</style>
```

- 定位

```html
<html>
<div id="father">
    <div id="son">+</div>
</div>
</html>

<style>
    #father {
        position: relative;		// 啥都行 relative/absolute/fixed
        width: 400px;
        height: 400px;
        border: solid black 1px;
    }
    #son {
        position: absolute;		// 相对父元素 绝对
        bottom: 50%;
        left: 50%;
    }
</style>
```

