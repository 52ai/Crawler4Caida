# coding:utf-8
"""
Create on Dec 20, 2018 by Wayne Yu
Fun：破解普遍服务验证码爬取的新指定的信息
在此之前各个技术关键点均以攻克，下面对整个解决思路做一个梳理

第一步，读取uuid序列
第二步，打开firefox浏览器页面,并获取的到相关元素
第三步，循环读取（先采用串行）uuid，并处理获取信息（需加异常处理）

处理函数：

1）填充相关元素
2）发起查询请求，并处理结果，提取信息，存储到结果列表

第四步，将结果列表写到文件中

"""
from selenium import webdriver
import pytesseract
from PIL import Image, ImageEnhance
import time
import csv


def get_page_info(query_uuid):
    print(driver.title)
    # 定位UUID
    uuid_input = driver.find_element_by_id("uuid")
    uuid_input.clear()
    uuid_input.send_keys(query_uuid)
    # time.sleep(3)
    # 截取屏幕保存到本地，然后提取验证码，作为输入
    driver.save_screenshot("screen.png")
    # 定位验证码的图片
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
    """
    此处需要加入异常处理，分两种，一种是识别失败（在main函数已处理），另一种是识别错误（抛异常）
    """
    image_number = pytesseract.image_to_string(sharp_img)  # 在windows下需要先安装tesseract-ocr程序，并修改pytesseract.py
    print("image_number:", image_number)
    # 定位验证码输入框
    checkcode_input = driver.find_element_by_id("checkcode")
    checkcode_input.clear()
    checkcode_input.send_keys(image_number)
    # time.sleep(3)
    btn_dev = driver.find_element_by_id("btn_dev")
    btn_dev.click()
    # print(driver.page_source)
    # time.sleep(3)
    table26 = driver.find_element_by_xpath('//div[@id="info"]/table/tbody/tr[2]/td[6]')
    str1 = table26.text
    table22 = driver.find_element_by_xpath('//div[@id="info"]/table/tbody/tr[2]/td[2]')
    str2 = table22.text
    table23 = driver.find_element_by_xpath('//div[@id="info"]/table/tbody/tr[2]/td[3]')
    str3 = table23.text
    table24 = driver.find_element_by_xpath('//div[@id="info"]/table/tbody/tr[2]/td[4]')
    str4 = table24.text
    table25 = driver.find_element_by_xpath('//div[@id="info"]/table/tbody/tr[2]/td[5]')
    str5 = table25.text
    table26 = driver.find_element_by_xpath('//div[@id="info"]/table/tbody/tr[2]/td[6]')
    str6 = table26.text
    table27 = driver.find_element_by_xpath('//div[@id="info"]/table/tbody/tr[2]/td[7]')
    str7 = table27.text
    table28 = driver.find_element_by_xpath('//div[@id="info"]/table/tbody/tr[2]/td[8]')
    str8 = table28.text
    table29 = driver.find_element_by_xpath('//div[@id="info"]/table/tbody/tr[2]/td[9]')
    str9 = table29.text
    table52 = driver.find_element_by_xpath('//div[@id="info"]/table/tbody/tr[5]/td[2]')
    str10 = table52.text
    line_str = [query_uuid, str1, str2, str3, str4, str5, str6, str7, str8, str9, str10]
    print(line_str)
    result.append(line_str)


if __name__ == "__main__":
    except_uuid = []
    result = []  # 最终需要的结果
    time_start = time.time()  # 记录启动时间
    result_file = "./result_all.csv"
    # 启动浏览器，并访问指定网址
    driver = webdriver.Firefox()
    driver.get("http://www.bbums.cn/busrvmanager/query.jsp")
    uuid_f = open("uuid.csv", "r", encoding='utf-8')
    for uuid in uuid_f.readlines():
        print(uuid.strip())
        # 刷新验证码
        driver.get("http://www.bbums.cn/busrvmanager/query.jsp")
        """
        异常处理：最大进行5次重复识别，如果连续5次识别失败那就记录在except_uuid列表中
        """
        try:
            get_page_info(uuid.strip())
        except BaseException:
            try:
                driver.get("http://www.bbums.cn/busrvmanager/query.jsp")
                get_page_info(uuid.strip())
            except BaseException:
                try:
                    driver.get("http://www.bbums.cn/busrvmanager/query.jsp")
                    get_page_info(uuid.strip())
                except BaseException:
                    try:
                        driver.get("http://www.bbums.cn/busrvmanager/query.jsp")
                        get_page_info(uuid.strip())
                    except BaseException:
                        try:
                            driver.get("http://www.bbums.cn/busrvmanager/query.jsp")
                            get_page_info(uuid.strip())
                        except BaseException:
                            except_uuid.append(uuid.strip())
    uuid_f.close()
    print(result)
    # 写文件
    f = open(result_file, "w", newline='', encoding='utf-8')
    writer = csv.writer(f)
    for item in result:
        writer.writerow(item)
    f.close()
    print(except_uuid)
    driver.quit()
    time_end = time.time()  # 记录结束时间
    print("=>SCRIPTS FINISH:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_end)), ", TIME CONSUMING：", (time_end - time_start), "s")

"""
无法识别时报的错：
Traceback (most recent call last):
  File "D:/Code/Crawler4Caida/automation/007Crawler4UniversalService/refactoring.py", line 67, in <module>
    get_page_info(uuid.strip())
  File "D:/Code/Crawler4Caida/automation/007Crawler4UniversalService/refactoring.py", line 56, in get_page_info
    print(driver.page_source)
  File "……\webdriver.py", line 679, in page_source
    return self.execute(Command.GET_PAGE_SOURCE)['value']
  File "……\webdriver.py", line 321, in execute
    self.error_handler.check_response(response)
  File "……\errorhandler.py", line 241, in check_response
    raise exception_class(message, screen, stacktrace, alert_text)
selenium.common.exceptions.UnexpectedAlertPresentException: Alert Text: None
Message: 

"""