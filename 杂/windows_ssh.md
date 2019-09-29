# windows ssh 配置
- 直接WSL登录，不需要配置，需要把windows的wsl功能打开
- 下载windows的openssh功能并打开（自行百度），配置ssh_config或者config文件

## WSL
略，进去就能用

## ssh 配置的地址
- 全局地址
C:\ProgramData\ssh\ssh_config
- 用户地址
C:\Users\wangd\.ssh\config

配置的写法，写这两个就够了，都写在全局配置下，用户配置可以不写
```
// 正常的ssh方式``ssh my_user_name@123.234.000``
Host alias
    HostName hostname
    User user

// 可以直接输入``ssh Myth``登录
Host Myth
    HostName 123.234.000
    User [my_user_name]
```