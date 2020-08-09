参考stackoverflow
https://stackoverflow.com/questions/16365130/what-is-the-difference-between-usr-bin-env-bash-and-usr-bin-bash

python：
https://stackoverflow.com/questions/4377109/shell-script-execute-a-python-program-from-within-a-shell-script

## 结论
``#!/usr/bin/env bash``更灵活
``#!/usr/bin/bash``更安全，具体

一般情况下用第一个方便一点

```
#!/bin/sh
python python_script.py
```