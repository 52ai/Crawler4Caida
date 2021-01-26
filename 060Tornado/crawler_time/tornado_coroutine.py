# coding:utf-8
"""
create on Jan 25, 2021 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

基于Tornado的coroutine并发爬取

"""

HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
   'Accept-Language': 'zh-CN,zh;q=0.8',
   'Accept-Encoding': 'gzip, deflate',}

URLS = ['http://www.cnblogs.com/moodlxs/p/3248890.html', 
        'https://www.zhihu.com/topic/19804387/newest',
        'http://blog.csdn.net/yueguanghaidao/article/details/24281751',
        'https://my.oschina.net/visualgui823/blog/36987',
        'http://blog.chinaunix.net/uid-9162199-id-4738168.html',
        'http://www.tuicool.com/articles/u67Bz26',
        'http://rfyiamcool.blog.51cto.com/1030776/1538367/',
        'http://itindex.net/detail/26512-flask-tornado-gevent',
        'http://www.cnblogs.com/moodlxs/p/3248890.html', 
        'https://www.zhihu.com/topic/19804387/newest',
        'http://blog.csdn.net/yueguanghaidao/article/details/24281751',
        'https://my.oschina.net/visualgui823/blog/36987',
        'http://blog.chinaunix.net/uid-9162199-id-4738168.html',
        'http://www.tuicool.com/articles/u67Bz26',
        'http://rfyiamcool.blog.51cto.com/1030776/1538367/',
        'http://itindex.net/detail/26512-flask-tornado-gevent',
        'http://www.cnblogs.com/moodlxs/p/3248890.html', 
        'https://www.zhihu.com/topic/19804387/newest',
        'http://blog.csdn.net/yueguanghaidao/article/details/24281751',
        'https://my.oschina.net/visualgui823/blog/36987',
        'http://blog.chinaunix.net/uid-9162199-id-4738168.html',
        'http://www.tuicool.com/articles/u67Bz26',
        'http://rfyiamcool.blog.51cto.com/1030776/1538367/',
        'http://itindex.net/detail/26512-flask-tornado-gevent',
        'http://www.cnblogs.com/moodlxs/p/3248890.html', 
        'https://www.zhihu.com/topic/19804387/newest',
        'http://blog.csdn.net/yueguanghaidao/article/details/24281751',
        'https://my.oschina.net/visualgui823/blog/36987',
        'http://blog.chinaunix.net/uid-9162199-id-4738168.html',
        'http://www.tuicool.com/articles/u67Bz26',
        'http://rfyiamcool.blog.51cto.com/1030776/1538367/',
        'http://itindex.net/detail/26512-flask-tornado-gevent',
        'http://www.cnblogs.com/moodlxs/p/3248890.html', 
        'https://www.zhihu.com/topic/19804387/newest',
        'http://blog.csdn.net/yueguanghaidao/article/details/24281751',
        'https://my.oschina.net/visualgui823/blog/36987',
        'http://blog.chinaunix.net/uid-9162199-id-4738168.html',
        'http://www.tuicool.com/articles/u67Bz26',
        'http://rfyiamcool.blog.51cto.com/1030776/1538367/',
        'http://itindex.net/detail/26512-flask-tornado-gevent',
        'http://www.cnblogs.com/moodlxs/p/3248890.html', 
        'https://www.zhihu.com/topic/19804387/newest',
        'http://blog.csdn.net/yueguanghaidao/article/details/24281751',
        'https://my.oschina.net/visualgui823/blog/36987',
        'http://blog.chinaunix.net/uid-9162199-id-4738168.html',
        'http://www.tuicool.com/articles/u67Bz26',
        'http://rfyiamcool.blog.51cto.com/1030776/1538367/',
        'http://itindex.net/detail/26512-flask-tornado-gevent',
        'http://www.cnblogs.com/moodlxs/p/3248890.html', 
        'https://www.zhihu.com/topic/19804387/newest',
        'http://blog.csdn.net/yueguanghaidao/article/details/24281751',
        'https://my.oschina.net/visualgui823/blog/36987',
        'http://blog.chinaunix.net/uid-9162199-id-4738168.html',
        'http://www.tuicool.com/articles/u67Bz26',
        'http://rfyiamcool.blog.51cto.com/1030776/1538367/',
        'http://itindex.net/detail/26512-flask-tornado-gevent']


# URLS = ['https://www.google.com.hk/maps/search/beijing,China/', 'https://www.baidu.com/']

import time 
from tornado.gen import coroutine
from tornado.ioloop import IOLoop
from tornado.httpclient import AsyncHTTPClient, HTTPError
from tornado.httpclient import HTTPRequest

#urls与前面相同
class MyClass(object):

    def __init__(self):
        #AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
        self.http = AsyncHTTPClient()

    @coroutine  
    def get(self, url):
        #tornado会自动在请求首部带上host首部        
        request = HTTPRequest(url=url,
                            method='GET',
                            headers=HEADERS,
                            connect_timeout=2.0,
                            request_timeout=2.0,
                            follow_redirects=False,
                            max_redirects=False,
                            user_agent="Mozilla/5.0+(Windows+NT+6.2;+WOW64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/45.0.2454.101+Safari/537.36",)
        response = yield self.http.fetch(request, raise_error=False)
        self.find(response)

    def find(self, response):
        if response.error:
            print(response.error)
        print(response.code, response.effective_url, response.request_time)


class Download(object):

    def __init__(self):
        self.a = MyClass()
        self.urls = URLS

    @coroutine
    def d(self):
        print(u'基于tornado的并发抓取')        
        t1 = time.time()
        yield [self.a.get(url) for url in self.urls]
        t = time.time() - t1
        print(t)

if __name__ == '__main__':
    dd = Download()
    loop = IOLoop.current()
    loop.run_sync(dd.d)