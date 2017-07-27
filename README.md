
# http

http server that takes a dictionary with callbacks to functions based on paths and resolves parameters

```
d = {
    'test': test
}
http.serve(d)

```
```
******************** Request ********************
['GET /test?a=3 HTTP/1.1', 'Host: 192.168.1.112', 'Connection: keep-alive', 'Accept-Encoding: gzip, deflate', 'Accept: */*', 'User-Agent: HTTPie/0.9.8', '', '']
******************** Request ********************
PATH:  test
PARAMS:  {'a': '3'}
Calling test(a='3')
```


# KtoRGB

color temperature to rgb for neopixel
