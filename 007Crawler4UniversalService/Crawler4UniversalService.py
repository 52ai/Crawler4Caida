# coding:utf-8
"""
create on December 19, 2018 by Wayne Yu
"""
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.request import urlretrieve
import pytesseract
from PIL import Image, ImageEnhance
import time

driver = webdriver.Firefox()
driver.get("http://www.bbums.cn/busrvmanager/query.jsp")
print(driver.title)
uuid_input = driver.find_element_by_id("uuid")
uuid_input.send_keys("d75aaa83-d4de-1544-975f-407d0f289335	")
# time.sleep(3)

# 截取屏幕保存到本地，然后提取验证码，作为输入
driver.save_screenshot("screen.png")
# 定位验证码
checkcode_img = driver.find_element_by_id("checkcode2")
location = checkcode_img.location  # 获取验证码的x,y坐标
size = checkcode_img.size  # 获取验证码的长宽
rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
          int(location['y'] + size['height']))  # 生成需截取的位置坐标
i = Image.open("screen.png")  # 打开截图
frame_crop = i.crop(rangle)  # 截取指定区域
frame_crop.save('checkcode_crop.png')  # 保存截取的验证码

# 获取验证码图片，并进行识别
imageCode = Image.open("checkcode_crop.png")
sharp_img = ImageEnhance.Contrast(imageCode).enhance(2.0)  # 图片增强并二值化
sharp_img.save("sharp_img.png")
image_number = pytesseract.image_to_string(sharp_img)  # 在windows下需要先安装tesseract-ocr程序，并修改pytesseract.py
print("image_number:", image_number)
checkcode_input = driver.find_element_by_id("checkcode")
checkcode_input.send_keys(image_number)
# time.sleep(3)
btn_dev = driver.find_element_by_id("btn_dev")
btn_dev.click()
print(driver.page_source)
div_table = driver.find_element_by_xpath('//div[@id="info"]/table/tbody/tr[5]/td[2]')
print(div_table.text)
time.sleep(3)
driver.quit()

# find the element that's name attribute is q (the google search box)
# inputElement = driver.find_element_by_name("q")  # equal to the method: find_element(By.NAME, "q")
# inputElement = driver.find_element(By.NAME, "q")
# type in the search
# inputElement.send_keys("cheese!")
# Getting text values
# print(inputElement.text)
# submit the form
# inputElement.submit()
# try:
#     WebDriverWait(driver, 10).until(EC.title_contains("cheese!"))
#     print(driver.title)
#     # Next Step Learn JavaScripts, Js is very useful in web crawler
#     driver.execute_script('window.alert("Hello, JavaScripts!---By Wayne Yu 2018.11.14");')
#     time.sleep(10)
# finally:
#     driver.quit()

