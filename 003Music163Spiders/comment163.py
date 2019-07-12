# encoding=utf-8
"""
这段代码竟然可以爬到数据
这里面肯定是有问题的，有空再好好研究下，最起码说明方向没有错
走selenium技术路线也是对的
下一步工作就是找个时间，好好的规划下对于网易云音乐的数据爬取及分析的思路
不过在此之前，先把几个关键的技术点攻破
形成爬取->存储->分析->输出的一条龙服务，最最关键就是要有好的idea
以此作为开始吧，仿佛看到了曙光
"""
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time

driver = webdriver.Firefox()
driver.maximize_window()
driver.set_page_load_timeout(10)
try:
    driver.get("http://music.163.com/#/song?id=31877470")
except TimeoutException:
    print("time out of 10 s")
    driver.execute_script('window.stop()')

print(u"休眠结束")
driver.switch_to.frame("contentFrame")
time.sleep(5)
print(driver.find_element_by_id('comment-box').text)
bsObj = BeautifulSoup(driver.page_source)
source = driver.page_source
open('163.txt','w', encoding='utf-8').write(source)
driver.quit()
