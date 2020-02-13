# coding:utf-8
"""
create on Feb 12, 2019 By Wayne YU
Function:

爬取知识工厂中的相关数据用于地图基础课题的绘制

暂包括软课题、专报

"""
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv


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
        writer = csv.writer(csvFile, delimiter=",")
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
    time.sleep(3)  # 延迟加载等待页面加载完毕
    page_html = driver.page_source
    bsObj = BeautifulSoup(page_html, "html.parser")
    keti_info = bsObj.find("div", {"class": "ketiBox"})
    keti_content = bsObj.find("div", {"class": "xilanArticle"})


def gain_page_list(page_url):
    """
    根据传入的page_url，获取page_list
    :param page_url:
    :return page_list:
    """
    page_list = []
    print(page_url)
    driver.get(page_url)
    time.sleep(3)  # 延迟加载等待页面加载完毕
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
    for item in li_list:
        project_name = item.get_text()
        project_page_url = "http://k.caict.ac.cn" + item.find("a").attrs['href']
        print(project_name, project_page_url)
        # gain_page_info(project_page_url)
        tempt_list.append(project_name)
        tempt_list.append(project_page_url)
        page_list_save.append(tempt_list)
        tempt_list = []
    # 存储page_list_save
    save_path = "..\\000LocalData\\caict_k\\keti_list.csv"
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

        time.sleep(200)
        # 关闭当前窗口
        driver.close()
        # 切回到vpn窗口
        driver.switch_to.window(vpn_handle)
        # # 自动退出
        # vpn_logout = driver.find_element_by_xpath("//*[@_html='注销']")
        # vpn_logout.click()

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




