# Nodemcu: Interfacing with a 4×4 Matrix Keypad

参考：
https://diyi0t.com/keypad-tutorial-for-arduino-and-esp8266/
https://techtutorialsx.com/2017/03/18/esp8266-interfacing-with-a-4x4-matrix-keypad/

https://embedjournal.com/interface-4x4-matrix-keypad-with-microcontroller/

# 数字键盘电路

![](https://i.imgur.com/uvUNVSx.png)

# 准备工作
1. 准备好硬件，接线
1. 安装库： Keypad library of Mark Stanley and Alexander Brevig 

![](https://i.imgur.com/ZuSsNH5.png)
note: 图中这个接线有点问题，应该接D0~D7。
代码中
```C
byte rowPins[ROWS] = {D7, D6, D5, D4}; 
byte colPins[COLS] = {D3, D2, D1, D0}; 
```
D1~D8有bug，可能是我的usb线又要当电源又要当input/output，pins数量不够

> 如何在Arduino IDE中安装库：
https://diyi0t.com/how-to-install-a-library-in-the-arduino-ide/

# 代码
nodemcu串口波特率用115200
注意监视器也要调成115200

```C
#include "Keypad.h"
const byte ROWS = 4; //four rows
const byte COLS = 4; //four columns

// define the 2d keys
char keys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};

byte rowPins[ROWS] = {D7, D6, D5, D4}; 
byte colPins[COLS] = {D3, D2, D1, D0}; 

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

void setup() {
  Serial.begin(115200);
}

void loop() {
  char key = keypad.getKey();

  if (key){
    Serial.println("Key is: ");
    Serial.println(key);
  }
}
```

![](https://i.imgur.com/Ld9rhob.png)



