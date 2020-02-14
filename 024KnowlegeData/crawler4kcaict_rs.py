# coding:utf-8
"""
create on Feb 13, 2020 By Wayne YU
Function:

爬取院知识工厂中软课题研究成果<research_subject>
爬取包括7项内容:
课题名称（subject_name）、
课题编号（subject_number）、
课题时间（subject_time）、
负责人（responsible_person）、
负责单位（responsible_dep）、
课题类别（subject_classification）、
课题内容（subject_content）


"""
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import re


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return: None
    """
    print("write file <%s> ..." % des_path)
    csvFile = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csvFile, delimiter="|")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csvFile.close()
    print("write finish!")


def gain_page_info(page_url):
    """
    根据传入的page_url，获取page_info
    :param page_url:
    :return page_info:
    """
    page_info = []
    driver.get(page_url)
    time.sleep(1)  # 延迟加载等待页面加载完毕
    page_html = driver.page_source
    bsObj = BeautifulSoup(page_html, "html.parser")
    subject_info = bsObj.find("div", {"class": "ketiBox"})
    subject_info_text = subject_info.get_text()
    subject_info_text = subject_info_text.strip().split("\n")
    subject_info_str = subject_info_text[0]
    subject_info_str = subject_info_str.strip().split("：")
    # print(subject_info_str)
    cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")
    subject_classification = subject_info_str[1].split("\xa0\xa0\xa0")[0]
    subject_classification = str(subject_classification)
    subject_classification = cop.sub('', subject_classification)
    responsible_dep = subject_info_str[-1]
    responsible_dep = str(responsible_dep)
    responsible_dep = cop.sub('', responsible_dep)
    print(subject_classification)
    print(responsible_dep)
    page_info.append(responsible_dep)
    page_info.append(subject_classification)
    subject_content = bsObj.find("div", {"class": "xilanArticle"})
    subject_content = subject_content.findAll("p")
    # print(subject_content)
    # print(len(subject_content))
    # print("-------------------------------")
    subject_content_info = ""
    for item in subject_content[0:len(subject_content)-1]:
        print(item)
        subject_content_info = subject_content_info + str(item)
    page_info.append(subject_content_info)
    return page_info


def gain_page_list(page_url):
    """
    根据传入的page_url，获取page_list
    :param page_url:
    :return page_list:
    """
    page_list = []
    print(page_url)
    driver.get(page_url)
    # time.sleep(3)  # 延迟加载等待页面加载完毕
    # 获取页面html信息
    # page_html = driver.page_source
    # bsObj = BeautifulSoup(page_html, "html.parser")
    # # more_btn_text = bsObj.find("div", {"class": "moreBtn"}).get_text()
    while True:
        # 若没加载完成则需要下拉到底部
        bottom_js = "var q=document.documentElement.scrollTop=10000000000"
        driver.execute_script(bottom_js)
        time.sleep(0.001)
        page_html = driver.page_source
        bsObj = BeautifulSoup(page_html, "html.parser")
        more_btn_text = bsObj.find("div", {"class": "moreBtn"}).get_text()
        # print(more_btn_text)
        if more_btn_text == "全部加载完成！":
            break
    print(more_btn_text)
    # 加载完成后，需要获取软课题url列表
    page_list_save = []
    tempt_list = []
    page_html = driver.page_source
    bsObj = BeautifulSoup(page_html, "html.parser")
    li_list = bsObj.find("div", {"class": "bd sgUL"}).find("ul")
    # 寻找断点
    break_cnt = 0
    for item in li_list:
        item_a = item.find("a").get_text()
        item_a = item_a.strip().split(" ")
        if len(item_a) == 2:
            subject_name = item_a[1]
        else:
            break_cnt += 1
            continue
        if subject_name == "移动应用商店对信息产业的发展影响分析":
            break
        break_cnt += 1

    run_cnt = 0
    for item in li_list:
        if run_cnt < break_cnt:
            run_cnt += 1
            continue
        try:
            item_a = item.find("a").get_text()
            item_a = item_a.strip().split(" ")
            if len(item_a) == 2:
                subject_name = item_a[1]
                subject_number = item_a[0]
                # 对课题编号的不规范情况做一些处理
                """
                规范命名2019-T-32，大致规范了下，有空还需做进一步处理
                """
                subject_number.replace("－", "-", 2)
                subject_number_split = subject_number.split("-")
                subject_time = subject_number_split[0]
                if len(subject_time) != 4:
                    subject_time = subject_time[0:4]
                    subject_number = subject_number[0:4] + "-" + subject_number[4:4] + "-" + subject_number[5:]
                    subject_number.replace("--", "-", 2)
            else:
                continue

            if len(item.find("span").get_text()) != 0:
                responsible_person = item.find("span").get_text()
            else:
                responsible_person = "None"

            subject_page_url = "http://k.caict.ac.cn" + item.find("a").attrs['href']
            print(subject_name, subject_number, subject_time, responsible_person, subject_page_url)
            page_info_list = gain_page_info(subject_page_url)
            tempt_list.append(subject_name)
            tempt_list.append(subject_number)
            tempt_list.append(subject_time)
            tempt_list.append(responsible_person)
            tempt_list.extend(page_info_list)
            tempt_list.append(subject_page_url)
            page_list_save.append(tempt_list)
            tempt_list = []
        except Exception as e_log:
            print("ERROR:", e_log)
            continue
        finally:
            # 存储page_list_save
            save_path = "..\\000LocalData\\caict_k\\research_subject.csv"
            write_to_csv(page_list_save, save_path)
    return page_list


def login_knowledge_factory(page_url):
    """
    根据传入的url，使用VPN登录知识工厂
    :param page_url:
    :return result_list:
    """
    result_list = []
    driver.get(page_url)
    # 获取用户名和密码
    login_pwd_file = "..\\000LocalData\\caict_k\\login.csv"
    file_read = open(login_pwd_file, 'r', encoding='utf-8')
    user_name_list = []
    user_password_list = []
    for line in file_read.readlines():
        line = line.strip().split(',')
        user_name_list.append(line[0])
        user_password_list.append(line[1])
    user_name = user_name_list[0]
    user_password = user_password_list[0]
    time.sleep(1)
    try:
        login_username = driver.find_element_by_id("svpn_name")
        login_username.send_keys(user_name)
        time.sleep(1)
        login_password = driver.find_element_by_id("svpn_password")
        login_password.send_keys(user_password)
        time.sleep(1)
        login_button = driver.find_element_by_id("logButton")
        login_button.click()
        time.sleep(10)
        # 登陆VPN成功，进入知识工厂(涉及到多个窗口的问题)
        k_click = driver.find_element_by_xpath("//*[@rcid='165']")
        k_click.click()
        time.sleep(10)
        # print(driver.page_source)
        # 输出当前窗口的句柄
        vpn_handle = driver.current_window_handle
        # 获取当前窗口句柄集合<列表类型>
        handles = driver.window_handles
        k_handle = handles[1]  # 获取第二个窗口的句柄，即第二窗口
        # 切换到k_handle
        driver.switch_to.window(k_handle)

        login_username_k = driver.find_element_by_id("loginKey")
        login_username_k.send_keys(user_name)
        time.sleep(1)
        login_password_k = driver.find_element_by_id("password")
        login_password_k.send_keys(user_password)
        time.sleep(1)
        login_button_k = driver.find_element_by_id("submitLoginBtn")
        login_button_k.click()
        time.sleep(3)
        # 知识工厂登录成功，开始进入知识爬取页面
        kjcg_url = "http://k.caict.ac.cn/ekp/caict/km/zhaochengguo/kjcg/"
        page_list_info = gain_page_list(kjcg_url)
        print(page_list_info)

        time.sleep(10)
        # 关闭当前窗口
        driver.close()
        # 切回到vpn窗口
        driver.switch_to.window(vpn_handle)
        # # 自动退出
        vpn_logout = driver.find_element_by_xpath("//*[@_html='注销']")
        vpn_logout.click()

    except BaseException as e_log:
        print(e_log)
    time.sleep(200)  # 延迟加载等待页面加载完毕
    return result_list


if __name__ == "__main__":
    web_url = "https://vpn.caict.ac.cn/por/service.csp"
    time_start = time.time()
    # 启动浏览器，开始登陆知识工厂（需先登陆VPN）
    driver = webdriver.Firefox()
    try:
        crawler_result_list = login_knowledge_factory(web_url)
        print(crawler_result_list)
    except Exception as e:
        print(e)
    # 关闭浏览器
    driver.quit()
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end-time_start), "S")




