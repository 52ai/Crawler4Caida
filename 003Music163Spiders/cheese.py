# coding:utf-8
"""
create on Nov 14, 2018 by Wayne Yu
"""
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.get("http://www.google.com")
print(driver.title)
# find the element that's name attribute is q (the google search box)
# inputElement = driver.find_element_by_name("q")  # equal to the method: find_element(By.NAME, "q")
inputElement = driver.find_element(By.NAME, "q")
# type in the search
inputElement.send_keys("cheese!")
# Getting text values
print(inputElement.text)
# submit the form
inputElement.submit()
try:
    WebDriverWait(driver, 10).until(EC.title_contains("cheese!"))
    print(driver.title)
    # Next Step Learn JavaScripts, Js is very useful in web crawler
    driver.execute_script('window.alert("Hello, JavaScripts!---By Wayne Yu 2018.11.14");')
    time.sleep(10)
finally:
    driver.quit()

