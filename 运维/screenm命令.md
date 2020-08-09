https://www.runoob.com/linux/linux-comm-screen.html

```
# 创建
screen -S [Name]

# 挂起
Ctrl+a 再按 d

# c查看
screen -ls

# 重新连接
screen -r [ID]

# 结束
screen -X -S [ID] quit
```