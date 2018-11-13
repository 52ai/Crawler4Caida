# coding:utf-8
"""
Create on Nov 13, 2018 by Wayne Yu
Function: Get music 163 artists info
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import csv
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


def get_artists_info(url):
    # html = urlopen(url)
    caps = webdriver.DesiredCapabilities().FIREFOX
    caps['marionette'] = True
    binary = FirefoxBinary(r'C:\\Program Files\\Mozilla Firefox\\firefox.exe')
    driver = webdriver.Firefox(firefox_binary=binary, capabilities=caps)
    html = driver.get(url)
    print(html)
    # bs_obj = BeautifulSoup(html.read(), "html5lib")
    # print(bs_obj)
    driver.close()
    return "OK!"


if __name__ == "__main__":
    page_url = "https://music.163.com/#/artist?id=8103"
    print(get_artists_info(page_url))
