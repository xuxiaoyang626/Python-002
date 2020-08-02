# 学习笔记

## 系统代理IP：
* export http_proxy='http://52.179.231.206:80'
* setting 增加 scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware
* 通过 Request.meta['proxy'] 读取 http_proxy 环境变量加载代理

*免费代理IP* https://github.com/zqHero/FreeIpAgent

## 编写中间件
**重写以下的方法**
* process_request(request, spider)
* process_response(request, response, spider)
* process_exception(request, response, spider)
* process_cwarler(cls, crawler)