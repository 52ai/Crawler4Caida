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

本次版本加入并发！20个线程

"""
from selenium import webdriver
import pytesseract
from PIL import Image, ImageEnhance
import time
import csv
import threading
from selenium.webdriver.firefox.options import Options

n_threading = 3  # 并发线程数
except_uuid = []
result = []  # 最终需要的结果
uuid_all = []  # 存储所有uu_id
uuid_piece = []  # 存储按线程数分配后的结果
run_index_group = [0] * n_threading  # 存储组内坐标类表，初始化为0


def get_page_info(query_uuid, driver, uuid_num, run_index):
    # print(driver.title)
    # 定位UUID
    uuid_input = driver.find_element_by_id("uuid")
    uuid_input.clear()
    uuid_input.send_keys(query_uuid)
    # time.sleep(3)
    # 截取屏幕保存到本地，然后提取验证码，作为输入
    screen_png_name = "screen"+str(run_index)+".png"
    print(screen_png_name)
    driver.save_screenshot(screen_png_name)
    # 定位验证码的图片
    checkcode_img = driver.find_element_by_id("checkcode2")
    location = checkcode_img.location  # 获取验证码的x,y坐标
    size = checkcode_img.size  # 获取验证码的长宽
    rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
              int(location['y'] + size['height']))  # 生成需截取的位置坐标
    i = Image.open(screen_png_name)  # 打开截图
    frame_crop = i.crop(rangle)  # 截取指定区域
    checkcode_png_name = "checkcode_crop_"+str(run_index)+".png"
    frame_crop.save(checkcode_png_name)  # 保存截取的验证码

    # 获取验证码图片，并进行识别
    imageCode = Image.open(checkcode_png_name)
    sharp_img = ImageEnhance.Contrast(imageCode).enhance(2.0)  # 图片增强并二值化
    # sharp_png_name = run_index + "_sharp_img.png"
    # sharp_img.save(sharp_png_name)
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
    # print(line_str)
    result[uuid_num] = line_str


def run_crawler(run_index, max_cnt):
    # 启动浏览器，并访问指定网址
    fire_options = Options()
    fire_options.headless = True
    driver = webdriver.Firefox(options=fire_options)   # 使用无头浏览器速度并没有加快很多
    # driver = webdriver.Firefox()
    driver.get("http://www.bbums.cn/busrvmanager/query.jsp")
    for run_item in uuid_piece[run_index]:
        # print(run_item, run_index, max_cnt, run_index_group[run_index])
        uuid_num = run_index * max_cnt + run_index_group[run_index]
        print("uuid_num:", uuid_num)
        # 刷新验证码
        driver.get("http://www.bbums.cn/busrvmanager/query.jsp")
        """
               异常处理：最大进行5次重复识别，如果连续5次识别失败那就记录在except_uuid列表中
        """
        try:
            get_page_info(run_item, driver, uuid_num, run_index)
        except BaseException:
            try:
                driver.get("http://www.bbums.cn/busrvmanager/query.jsp")
                get_page_info(run_item, driver, uuid_num, run_index)
            except BaseException:
                try:
                    driver.get("http://www.bbums.cn/busrvmanager/query.jsp")
                    get_page_info(run_item, driver, uuid_num, run_index)
                except BaseException:
                    try:
                        driver.get("http://www.bbums.cn/busrvmanager/query.jsp")
                        get_page_info(run_item, driver, uuid_num, run_index)
                    except BaseException:
                        try:
                            driver.get("http://www.bbums.cn/busrvmanager/query.jsp")
                            get_page_info(run_item, driver, uuid_num, run_index)
                        except BaseException:
                            except_uuid.append(run_item)
        run_index_group[run_index] += 1
    driver.quit()


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    result_file = "./result_all_plus_plus_plus.csv"
    # input_file = "./uuid.csv"
    # uuid_file = open(input_file, "r", encoding='utf-8')
    # for uuid in uuid_file.readlines():
    #     result.append("0")
    #     uuid_all.append(uuid.strip())
    # uuid_file.close()
    un_list = ['9e89f8da-1046-1b42-bfd2-3c784397a1d2', 'b32adcbe-9ca5-1d4d-b818-506f77211e8a', '1a420b6b-3bd2-1245-83a6-446a2e6f5523', 'd3af0b23-824b-1346-ae38-506f771e3908', '405e0a18-8266-1b49-85a5-bc3f8fe47e14', '34d835cc-62f5-134a-965f-3c784397b15c', 'c0fee38d-1aa3-1e4a-9c2d-407d0f28890d', '115adb72-9682-1f46-9f10-a0f4796109be', '27578767-3115-1045-a14c-506f7720cc2c', '5e979ab0-1812-1a45-98fd-a0f4792b2c08', '04c285c9-f56a-1044-be48-a0f479810960', '1502d5ff-249d-1342-9fc5-f898b98c79c4', '81ccb49e-fcc4-1a49-9f94-a0f4792b27b7', 'ed5fd35d-e486-144d-8aed-f898b98d195f', '510e8f9c-dd55-1f49-a391-407d0f27f248', '28366459-7821-1c40-8cb1-407d0f27b051', '4ce6b497-7a3a-1148-ac84-506f771e39cb']
    for uuid in un_list:
        result.append("0")
        uuid_all.append(uuid.strip())

    max_uuid_cnt = (len(uuid_all) // n_threading + 1)
    tmp_uuid_piece = []
    item_index = 1
    for item in uuid_all:
        if item_index % max_uuid_cnt != 0:
            tmp_uuid_piece.append(item)
        else:
            tmp_uuid_piece.append(item)
            uuid_piece.append(tmp_uuid_piece)
            tmp_uuid_piece = []
        item_index += 1
    if len(tmp_uuid_piece) != 0:
        uuid_piece.append(tmp_uuid_piece)
    # print(uuid_piece)

    # 读取拆分后的uuid列表，分别生成爬虫线程
    threads = []  # 存储进程
    item_index = 0
    for item in uuid_piece:
        print(item)
        threads.append(threading.Thread(target=run_crawler, args=(item_index, max_uuid_cnt)))
        item_index += 1
    print(item_index)
    for t in threads:
        t.setDaemon(True)
        t.start()
    # 必须等待for循环中所有线程都结束后再执行主线程
    for k in threads:
        k.join()
    print("All threading finished!")
    time_end = time.time()  # 记录结束时间
    print("=>SCRIPTS FINISH:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_end)), ", TIME CONSUMING：", (time_end - time_start), "s")
    # print(result)
    # 写文件
    f = open(result_file, "w", newline='', encoding='utf-8')
    writer = csv.writer(f)
    for item in result:
        writer.writerow(item)
    f.close()
    print(except_uuid)

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

实验1:100个uuid， 5个线程，耗时155s，未爬取个数7个
实验2:100个uuid，20个线程，耗时176s, 有线程卡死，无法统计
实验3:100个uuid， 8个线程，耗时147s，有线程卡死，无法统计
"""