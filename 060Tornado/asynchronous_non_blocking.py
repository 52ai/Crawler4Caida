# coding:utf-8
"""
create on Jan 22, 2021 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

因为搞自治域网络地理位置定位算法，涉及到大量数据爬取，数据太慢，需要借助异步非阻塞技术
调研了一圈，Tornado相当优秀，值得研究

Tornado有两种异步模式
1)add_callback。基于asyncio，资源消耗较少，性能还不错
2)run_in_executor。基于线程池/进程池，性能很好，但是资源消耗要高于add_callback的方案

"""
from tornado.ioloop import IOLoop, PeriodicCallback
import requests
import time
from concurrent.futures import ThreadPoolExecutor


# 业务逻辑操作
def job(id):
    """
    定义要干的事
    """
    # url = 'http://www.baidu.com/'
    # resp = requests.get(url)
    # print(resp.text)
    time.sleep(3)
    print("job:", id, ", finish!")


async def runner():
    """
    任务分发到异步非阻塞模型（Tornado）中
    """
    loop = IOLoop.current()
    exctutor = ThreadPoolExecutor(8000)
    # 此处开始任务分派
    for job_id in range(8000):
        loop.run_in_executor(exctutor, job, job_id)
    
    print('This will be excuted before loop finished.')


if __name__ == '__main__':
    time_start = time.time()
    IOLoop.current().run_sync(runner)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")




