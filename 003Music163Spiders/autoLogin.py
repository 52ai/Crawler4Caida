# coding:utf-8
"""
create on Nov 14, 2018 by Wayne Yu
Fun: auto login CRP and punch the clock

punchCard_roll = [["yuwenyan", "Yuwenyan2018"],
                  ["sujia", "Sujia0823"],
                  ["guanxin1", "Gx19890101"],
                  ["xuexue", "Zhuzhu19930114%"],
                  ["lijianmei", "19920329Jianmei"]]

"""
# coding:utf-8
from selenium import webdriver
import time
import re
from selenium.webdriver.firefox.options import Options

log_list = []
punchCard_roll = [["yuwenyan", "Yuwenyan2018"]]


def write_log(file_list, file_name):
    """
    将日志写到CSV 文件中
    :param file_list:
    :return: None
    """
    f = open(file_name, "a", newline='', encoding='utf-8')
    for log_line in file_list:
        f.write(log_line+"\n")
    f.close()


def punch_card(user_name, user_password):
    """
    punch card per person
    :param user_name:
    :param user_password:
    :return: None
    """
    # fire_options = Options()
    # fire_options.headless = True
    # driver = webdriver.Firefox(options=fire_options)   # 使用无头浏览器速度并没有加快很多
    driver = webdriver.Firefox()
    driver.get("https://crp.caict.ac.cn/seeyon/")
    time.sleep(3)
    # print(driver.title, "，login...")
    try:
        # WebDriverWait(driver, 10).until(EC.title_contains("余文艳"))
        # Next Step Learn JavaScripts, Js is very useful in web crawler
        # driver.execute_script('window.alert("Hello, JavaScripts!---By Wayne Yu 2018.11.14");')
        login_username = driver.find_element_by_id("login_username")
        login_username.send_keys(user_name)
        login_password = driver.find_element_by_id("login_password")
        login_password.send_keys(user_password)
        login_button = driver.find_element_by_id("login_button")
        login_button.click()
        # output current time and username
        print_name = re.findall(',(.*),', driver.title)
        # print(print_name)
        punch_time = time.time()
        punchCard = driver.find_element_by_id("appcenter_id")
        punchCard.click()
        # type in the search
        # inputElement.send_keys("cheese!")
        # Getting text values
        # print(inputElement.text)
        time.sleep(1)
    except BaseException:
        time.sleep(10)
        log_str = "打卡失败！"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))+" "+user_name
        log_list.append(log_str)
        print(log_str)
        return "Failed"
    finally:
        driver.quit()
    log_str = "打卡成功！"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(punch_time))+" "+print_name[0].strip()
    log_list.append(log_str)
    print(log_str)
    return "Success!"


if __name__ == "__main__":
    log_str = "Run Scripts(%s):" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    log_list.append(log_str)
    print(log_str)
    for item in punchCard_roll:
        # print(item[0], item[1])
        punch_card(item[0], item[1])
    log_str = "Scripts End(%s)!" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    log_list.append(log_str)
    print(log_str)
    # write log
    log_list.append("+++++++++++++++++++++++++++++++++++++++++\n")
    write_log(log_list, "log.csv")
    time.sleep(600)


