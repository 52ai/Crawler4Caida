# coding:utf-8
"""
create on Jan 2,2020 By Wayne Yu

Function:对Chrome的selenium进行测试

"""

from selenium import webdriver

browser = webdriver.Chrome()
browser.get('http://www.baidu.com/')