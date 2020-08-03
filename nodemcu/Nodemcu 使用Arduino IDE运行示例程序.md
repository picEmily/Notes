# Nodemcu 使用Arduino IDE运行示例程序

## 准备工作
1. 官网下载Arduino IDE
1. 连接Nodemcu到电脑

## 配置Arduino IDE

**首选项** 中在 **附加开发板管理器网址** 中填写``http://arduino.esp8266.com/stable/package_esp8266com_index.json``
![](https://i.imgur.com/XHmMMuK.png)

**工具》开发板》开发板管理器**中下载Nodemcu相关
![](https://i.imgur.com/qxhNSNv.png)

然后在**工具》开发板**选择自己的开发板
选择上传的端口（COM）
![](https://i.imgur.com/L6RUYxz.png)

## 上传示例文件
选择示例文件
![](https://i.imgur.com/0NlEv94.png)

上传
![](https://i.imgur.com/VIV7vNt.png)

# GPIO pins 

![](https://i.imgur.com/faZ66Ut.png)

在这个头文件里面定义了
https://github.com/esp8266/Arduino/blob/3e7b4b8e0cf4e1f7ad48104abfc42723b5e4f9be/variants/nodemcu/pins_arduino.h

# debug

## 串口通讯
串口通讯，nodemcu默认115200，注意串口监视器设置相同的比特率
例如
```C
void setup() {
	Serial.begin(115200);
}

void loop() {
	Serial.println("Hello World");
}
```

# 有意思的小网站
https://www.circuito.io/app?components=8653,9442,360216