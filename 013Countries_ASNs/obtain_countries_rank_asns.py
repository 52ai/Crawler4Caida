# coding:utf-8
"""
create on Oct 10,2019 by Wayne

Fun:获取全球各个国家的ASNs分配的数量、通道的数量以及ASN V4/V6地址的数量<数据来源：https://whois.ipip.net/countries>

"""
from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options

def obtain_info(page_url):
    """
    获取页面的信息，并处理
    :param page_url:
    :return:
    """
    driver.get(page_url)
    time.sleep(10)  # 延迟加载，等待页面的内容加载完毕
    # 获取页面的html信息
    page_html = driver.page_source
    print(page_html)


if __name__ == "__main__":
    web_url = "https://whois.ipip.net/countries"
    time_start = time.time()

    # 启动浏览器
    fire_options = Options()
    fire_options.headless = True
    driver = webdriver.Firefox(options=fire_options)
    driver.maximize_window()
    try:
        obtain_info(web_url)
    except Exception as e:
        print(e)
    # 关闭浏览器
    driver.quit()
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end-time_start), "S")
