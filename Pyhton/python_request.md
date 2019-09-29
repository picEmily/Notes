# Python Requests
https://2.python-requests.org/en/master/user/quickstart/
``pip3 install requests``

## Methods
### Quick Look
send request with http methods
- get: `r = requests.get(url)`
- post: `r = request.post(url)`

return value is a **responst** object
also, it has: 
- ``r = requests.put('http://httpbin.org/put', data = {'key':'value'})``
- ``r = requests.delete('http://httpbin.org/delete')``
- ``r = requests.head('http://httpbin.org/get')``
- ``r = requests.options('http://httpbin.org/get')``

### Methods Details
#### get
URL's query string

#### response content
```python3
r = requests.get('https://api.github.com/events')
# response的内容
# 这个东西就和``curl [url]``返回在terminal里面的结果一样
r.text
# 指定encoding
r.encoding
# 如果encoding在content里面(待学习:codecs module)
r.content
```

#### Deal with JSON data
- Check the response code(because Some servers may return a JSON object in a failed response)
``r.raise_for_status()``or ``r.status_code``
- ``r.json()`` returns a decoded json data(to list)

#### Raw Content
用到再说

#### Add http headers
```
url = 'https://api.github.com/some/endpoint'
headers = {'user-agent': 'my-app/0.0.1'}
r = requests.get(url, headers=headers)
```

#### Post with encoded data
either in *list* or *tuple*

#### Send with file
用到再说

#### Response Status Codes
可以直接返回status code, 也可以在错误的时候raise exception
```python3
# 返回status code
r.status_code()
# 如果是成功，返回None；如果失败raise exeption
r.raise_for_status()
```

#### 待学习
headers
cookies
history
...
