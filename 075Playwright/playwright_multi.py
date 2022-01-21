# coding:utf-8

"""
create on Jan 21, 2022 By Wayne YU
Function:

Test playwright

This are two mode of Playwright, synchronous(like Selenium) and asynchronous(like Pyppeteer)

"""
from playwright.sync_api import sync_playwright
import time
from concurrent.futures import ThreadPoolExecutor
import asyncio

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
        'http://www.cnblogs.com/moodlxs/p/3248890.html',
        'https://www.zhihu.com/topic/19804387/newest',
        'http://blog.csdn.net/yueguanghaidao/article/details/24281751',
        'https://my.oschina.net/visualgui823/blog/36987']


def job_spider(page_url, page_i):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(page_url)
            page.screenshot(path=f'screenshot-{page_i}.png')
            print(page.title())
            browser.close()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    star_time = time.time()
    # 同步模式大概70s
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor(4)
    tasks = []
    i = 0
    for url in URLS:
        i += 1
        task = loop.run_in_executor(executor, job_spider, url, i)
        tasks.append(task)
    loop.run_until_complete(asyncio.wait(tasks))
    print("time consuming:", (time.time() - star_time))
