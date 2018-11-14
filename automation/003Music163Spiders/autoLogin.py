# coding:utf-8
"""
create on Nov 14, 2018 by Wayne Yu
Fun: auto login CRP and punch the clock
"""
# coding:utf-8
from selenium import webdriver
import time

punCard_roll = [["yuwenyan", "123456"]]

driver = webdriver.Firefox()
driver.get("https://crp.caict.ac.cn/seeyon/index.jsp")
print(driver.title)
# find the element that's name attribute is q (the google search box)
# inputElement = driver.find_element_by_name("q")  # equal to the method: find_element(By.NAME, "q")
login_username = driver.find_element_by_id("login_username")
login_username.send_keys("yuwenyan")
login_password = driver.find_element_by_id("login_password")
login_password.send_keys("123456")
login_button = driver.find_element_by_id("login_button")
login_button.click()
# output current time and username
print(driver.title, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), "已打卡")
punchCard = driver.find_element_by_id("appcenter_id")
punchCard.click()
# type in the search
# inputElement.send_keys("cheese!")
# Getting text values
# print(inputElement.text)
# submit the form
# inputElement.submit()
try:
    # WebDriverWait(driver, 10).until(EC.title_contains("余文艳"))
    # Next Step Learn JavaScripts, Js is very useful in web crawler
    # driver.execute_script('window.alert("Hello, JavaScripts!---By Wayne Yu 2018.11.14");')
    time.sleep(20)
finally:
    driver.quit()

