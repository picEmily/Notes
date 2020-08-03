# Nodemcu http server

# 头文件
- ``#include <ESP8266WiFi.h>``
- ``#include <WiFiClient.h>``
- ``#include <ESP8266WebServer.h>``
- ``#include <ESP8266mDNS.h>``

## mDNS
Multicast DNS(多播DNS)
ESP作为web服务器，WIFI路由器为其分配地址，没有DNS服务器记录其域名。
多播DNS（mDNS）提供在没有任何传统单播DNS服务器的情况下在本地链路上执行类似DNS的操作的能力。此外，多播DNS指定DNS名称空间的一部分可供本地使用，无需支付任何年费，也无需设置授权或以其他方式配置传统DNS服务器来回答这些名称。

在ESP8266上使用本地网络中的mDNS
```C
if (MDNS.begin("esp8266")) {
Serial.println("MDNS responder started");
}
```
可以通过访问地址 http://esp8266.local 来访问服务器

## ESP8266WiFi
模式
- STA
- AP


```C
WiFi.mode(WIFI_STA);
WiFi.begin(ssid, password);

// wait for connection
while (WiFi.status() != WL_CONNECTED) {
	delay(500);
	Serial.print(".");
}
```

## Server and Client
### Client
https://blog.csdn.net/Naisu_kun/article/details/86761103\

```C
#include <WiFiClient.h>

WiFiClient client; 							// 声明一个客户端对象，用于与服务器进行连接
client.connect(serverIP, serverPort);		// 连接服务器
client.stop();								// 断开连接
```

### Server
https://blog.csdn.net/Naisu_kun/article/details/83179466

- 建立全局的Web服务器并监听某端口 ``ESP8266WebServer server(port)；``(port一般可写80);
- 在setup()中绑定http请求的回调函数 ``server.on(url, function);``
- 在setup()中绑定http请求不可用时的回调函数 ``server.onNotFound(function);``(可选);
- 在setup()中开启WebServer功能 ``server.begin();``
- 在loop()中监听客户请求并处理 ``server.handleClient();``

http请求的回调函数
```C
void homepage() {
  server.send(200, "text/plain", "Hello World");
}
```

完整示例
```C
#include <ESP8266WiFi.h>
// #include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

#ifndef STASSID
#define STASSID "dachui"
#define STAPSK  "wang960427"
#endif

const char *ssid = STASSID;
const char *password = STAPSK;

ESP8266WebServer server(80);    // 设置80端口

const int led = 13;

void handleRoot() {
  digitalWrite(led, 1);
  char temp[400];
  int sec = millis() / 1000;
  int min = sec / 60;
  int hr = min / 60;

  // int snprintf ( char * str, size_t size, const char * format, ... );
  // 设将可变参数(...)按照 format 格式化成字符串，
  // 并将字符串复制到 str 中，size 为要写入的字符的最大数目，超过 size 会被截断
  snprintf(temp, 400,

           "<html>\
  <head>\
    <meta http-equiv='refresh' content='5'/>\
    <title>ESP8266 Keypad</title>\
    <style>\
      body { background-color: #cccccc; font-family: Arial, Helvetica, Sans-Serif; Color: #000088; }\
    </style>\
  </head>\
  <body>\
    <h1>Hello from ESP8266!</h1>\
    <p>Uptime: %02d:%02d:%02d</p>\
    <img src=\"/test.svg\" />\
  </body>\
</html>",

           hr, min % 60, sec % 60
          );
  server.send(200, "text/html", temp);
  digitalWrite(led, 0);
}

void handleNotFound() {
  digitalWrite(led, 1);
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";

  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }

  server.send(404, "text/plain", message);
  digitalWrite(led, 0);
}

void drawGraph() {
  String out;
  out.reserve(2600);
  char temp[70];
  out += "<svg xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\" width=\"400\" height=\"150\">\n";
  out += "<rect width=\"400\" height=\"150\" fill=\"rgb(250, 230, 210)\" stroke-width=\"1\" stroke=\"rgb(0, 0, 0)\" />\n";
  out += "<g stroke=\"black\">\n";
  int y = rand() % 130;
  for (int x = 10; x < 390; x += 10) {
    int y2 = rand() % 130;
    sprintf(temp, "<line x1=\"%d\" y1=\"%d\" x2=\"%d\" y2=\"%d\" stroke-width=\"1\" />\n", x, 140 - y, x + 10, 140 - y2);
    out += temp;
    y = y2;
  }
  out += "</g>\n</svg>\n";

  server.send(200, "image/svg+xml", out);
}

void setup(void) {
  // connenct to WIFI
  pinMode(led, OUTPUT);                     // 设置led引脚为输出模式
  digitalWrite(led, 0);                     // led引脚设置为high
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  // print the WIFI connection info
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // mDNS enable us to use "esp8266.local" to connect this server
  if (MDNS.begin("esp8266")) {
    Serial.println("MDNS responder started");
  }

  // set routers
  server.on("/", handleRoot);
  server.on("/test.svg", drawGraph);
  server.on("/inline", []() {
    server.send(200, "text/plain", "this works as well");
  });
  server.onNotFound(handleNotFound);
  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  server.handleClient();
  MDNS.update();
}

```
