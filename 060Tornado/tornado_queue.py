# coding:utf-8
"""
create on Jan 22, 2021 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

探索Tornado异步网络爬虫技术

"""
import time
from datetime import timedelta

from html.parser import HTMLParser
from urllib.parse import urljoin, urldefrag

from tornado import gen, httpclient, ioloop, queues

base_url = "http://www.mryu.top/"
concurrency = 10


async def get_links_from_url(url):
    """Download the page at `url` and parse it for links.

    Returned links have had the fragment after `#` removed, and have been made
    absolute so, e.g. the URL 'gen.html#tornado.gen.coroutine' becomes
    'http://www.tornadoweb.org/en/stable/gen.html'.
    """
    response = await httpclient.AsyncHTTPClient().fetch(url)
    print("fetched %s" % url)

    html = response.body.decode(errors="ignore")
    return [urljoin(url, remove_fragment(new_url)) for new_url in get_links(html)]


def remove_fragment(url):
    pure_url, frag = urldefrag(url)
    return pure_url


def get_links(html):
    class URLSeeker(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.urls = []

        def handle_starttag(self, tag, attrs):
            href = dict(attrs).get("href")
            if href and tag == "a":
                self.urls.append(href)

    url_seeker = URLSeeker()
    url_seeker.feed(html)
    return url_seeker.urls


async def main():
    """
    异步执行主函数
    """
    q = queues.Queue()  # 定义队列， 先进先出
    start = time.time()  # 记录启动时间
    fetching, fetched, dead = set(), set(), set()  # 定义待获取，已获取，无法获取的集合

    async def fetch_url(current_url):
        """
        定义获取当前url连接的异步函数
        """
        if current_url in fetching:
            return

        print("fetching %s" % current_url)
        fetching.add(current_url)
        urls = await get_links_from_url(current_url)
        fetched.add(current_url)

        for new_url in urls:
            # Only follow links beneath the base URL
            if new_url.startswith(base_url):
                await q.put(new_url)  # 往队列中新增待获取的链接

    async def worker():
        async for url in q:
            if url is None:
                return
            try:
                await fetch_url(url)  # 获取内链
            except Exception as e:
                print("Exception: %s %s" % (e, url))
                dead.add(url)  # 内链获取异常
            finally:
                q.task_done()  # 计数器，每进入一个就加1，所以我们调用完了就减1

    await q.put(base_url)  # 程序刚启动，将base_url入队列

    # Start workers, then wait for the work queue to be empty.
    workers = gen.multi([worker() for _ in range(concurrency)])  # 启动协程，同时开启三个消费者
    await q.join(timeout=timedelta(seconds=300))  # 会阻塞，直到队列里没有数据为止
    assert fetching == (fetched | dead)
    print("Done in %d seconds, fetched %s URLs." % (time.time() - start, len(fetched)))
    print("Unable to fetch %s URLS." % len(dead))

    # Signal all the workers to exit.
    # 等待所有协程执行完毕
    for _ in range(concurrency):
        await q.put(None)
    await workers


if __name__ == "__main__":
    io_loop = ioloop.IOLoop.current()
    io_loop.run_sync(main)


"""
以此为案例，研究Tornado的异步爬虫技术

"""
