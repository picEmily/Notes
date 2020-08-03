# 购买域名
godaddy

# github page
加一个CNAME文件

./CNAME
```
# 不要加http:// www. 等，只写域名
xxxx.com
```

改完dns以后记得勾选强制https选项

# 改dns
主要是改dns，godaddy买的时候提供了dns服务器
当然也可以买别的
185.199.108.153~185.199.111.153是github page的ip

```
CNAME  www xxx.github.io
A      @   185.199.111.153
A      @   185.199.110.153
A      @   185.199.109.153
A      @   185.199.108.153
```
- CNAME：别名（将域名指向一个域名）
- A记录：将域名指向一个IPv4地址
- NS记录： 域名解析服务器记录，如果要将子域名指定某个域名服务器来解析，需要设置NS记录