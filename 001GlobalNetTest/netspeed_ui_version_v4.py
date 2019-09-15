# coding:utf-8
"""
由Wayne 创建于2019年9月11日
版本V4:主要在V3版本基础之上实现了一个UI界面
"""

from tkinter import *
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk

import subprocess
import threading
import time
import re
import csv
import socket


# ip_info 用于存储需要测试IP地址及其地理信息
ip_info = [["新加坡", "180.210.206.51"],
           ["马来西亚", "223.25.244.145"],
           ["越南", "45.117.76.22"],
           ["泰国", "43.254.132.221"],
           ["澳大利亚", "203.143.89.72"],
           ["印度", "149.129.138.11"],
           ["阿联酋", "185.93.245.1"],
           ["土耳其", "185.125.32.29"],
           ["沙特", "46.151.213.205"],
           ["哈萨克斯坦", "91.185.5.197"],
           ["蒙古", "43.231.113.234"],
           ["日本", "45.32.51.106"],
           ["韩国", "103.86.86.1"],
           ["香港", "203.119.87.218"],
           ["台湾", "218.32.21.1"],
           ["英国", "5.1.88.152"],
           ["德国", "185.72.247.76"],
           ["荷兰", "103.136.40.107"],
           ["俄罗斯", "46.38.51.201"],
           ["乌克兰", "91.229.78.83"],
           ["意大利", "192.71.26.35"],
           ["葡萄牙", "188.208.143.109"],
           ["芬兰", "185.87.108.247"],
           ["埃及", "41.215.240.13"],
           ["肯尼亚", "62.12.114.67"],
           ["尼日利亚", "154.113.1.27"],
           ["南非", "168.209.28.2"],
           ["美国", "45.35.23.120"],
           ["加拿大", "132.216.177.160"],
           ["墨西哥", "143.255.57.1"],
           ["巴西", "181.41.214.27"],
           ["阿根廷", "200.55.240.23"],
           ["智利", "190.105.239.70"]]

# lose_rate_list 用于存储丢包率，格式为country,ip,company1,company2,...,average
loss_rate_list = []
loss_rate_file = 'C:/ywyscripts/loss_rate.csv'
# time_delay_list 用于存储时延，格式为country,ip,company1,company2,...,average
time_delay_list = []
time_delay_file = 'C:/ywyscripts/time_delay.csv'

# log_list 用于存储所有log输出
log_list = []
log_file = 'C:/ywyscripts/log.txt'

# company_log_list 用于存储每个企业测试输出日志数据，用于备份使用
company_log_list = []
# 全局的拆分后的IP地址列表
ip_info_threading = []

n_threading = 11  # 设置并发线程数为11次
# 根据并发发线程数，拆分IP地址列表，按照等分，每轮的个数为IP列表总的个数除以并发数，向上取整
max_ip_cnt = (len(ip_info) // n_threading)
run_index_group = [0] * n_threading  # 存储组内坐标列表，初始化全为0


def run_ping_test(run_index):
    for run_item in ip_info_threading[run_index]:
        # print(run_item)
        # loss_rate, time_delay = run_ping(run_item[1])
        ftp_sub = subprocess.Popen("ping %s -n 1" % run_item[1],
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        ret = ftp_sub.stdout.read()
        str_ret = ret.decode('gbk')
        log_list.append(str_ret)
        # print(str_ret)
        # print("本组测试丢包率(", ip_str, ")：", re.findall('\d+%', str_ret)[0])
        # print("本组测试平均时延(", ip_str, ")：", re.findall('\d+ms', str_ret)[-1])

        try:
            loss_rate = re.findall('\d+%', str_ret)[0]
            time_delay = re.findall('\d+ms', str_ret)[-1]
        except IndexError:
            loss_rate = "NONE"
            time_delay = "INFINITE"
        log_str = "%s, %s, %s, %s" % (run_item[0], run_item[1], loss_rate, time_delay)
        company_log_list.append(log_str + "\n")
        # print(log_str)
        print(".", end='')
        loss_rate_list[run_index * max_ip_cnt + run_index_group[run_index]].append(loss_rate)  # 添加丢包率
        time_delay_list[run_index * max_ip_cnt + run_index_group[run_index]].append(time_delay)  # 添加时延
        run_index_group[run_index] += 1  # 组内索引自增1


def main_run():
    # 例：中亚-哈萨克斯坦/95.56.234.66
    # ip_str = "95.56.234.66"
    # run_ping_test(ip_str)
    # run_tracert_test(ip_str)
    # print("=>read loss_rate file, generate loss_rate_list")
    f_loss_rate = open(loss_rate_file, "r", encoding='utf-8')
    for line in f_loss_rate.readlines():
        # print(line.strip().split(','))
        loss_rate_list.append(line.strip().split(','))
    f_loss_rate.close()
    # print(loss_rate_list)

    # print("=>read time_delay file, generate time_delay_list")
    f_time_delay = open(time_delay_file, "r", encoding='utf-8')
    for line in f_time_delay.readlines():
        # print(line.strip().split(','))
        time_delay_list.append(line.strip().split(','))
    f_loss_rate.close()
    # print(time_delay_list)

    time_start = time.time()
    print("=>TEST START:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_start)))
    # print("country, ip, loss_rate, time_delay")
    # 下面开始读取IP地址列表进行ping测试，设置并发线程个数为n_threading
    tmp_ip_info = []
    item_index = 1
    for item in ip_info:
        if item_index % max_ip_cnt != 0:
            tmp_ip_info.append(item)
        else:
            tmp_ip_info.append(item)
            ip_info_threading.append(tmp_ip_info)
            tmp_ip_info = []
        item_index += 1
    if len(tmp_ip_info) != 0:
        ip_info_threading.append(tmp_ip_info)
    # print(ip_info_threading)
    # 根据并发线程数，拆分IP地址列表完毕，格式为[[[country, ip],[],[],[]],[],[],[]...]
    # item_index = 0
    # for item in ip_info:
    #     # print(item)
    #     loss_rate, time_delay = run_ping_test(item[1])
    #     log_str = "%s, %s, %s, %s" % (item[0], item[1], loss_rate, time_delay)
    #     company_log_list.append(log_str + "\n")
    #     print(log_str)
    #     loss_rate_list[item_index].append(loss_rate)  # 添加丢包率
    #     time_delay_list[item_index].append(time_delay)  # 添加时延
    #     item_index += 1  # 索引自增1
    # # print(len(ip_info))
    # 读取拆分后的IP地址列表，分别生成PING的测试线程
    threads = []  # 存储进程
    item_index = 0
    for item in ip_info_threading:
        # print(item)
        threads.append(threading.Thread(target=run_ping_test, args=(item_index,)))
        item_index += 1
    for t in threads:
        t.setDaemon(True)
        t.start()
    # 必须等待for循环里面的所有线程都结束后，再执行主线程
    for k in threads:
        k.join()
    print("All threading finished!")
    # print(loss_rate_list)
    # print(time_delay_list)
    time_end = time.time()
    print("=>TEST FINISH:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_end)), ", TIME CONSUMING：",
          (time_end - time_start), "s")

    # print("=>WRITE company_log")
    company_log_file = 'C:/ywyscripts/company_log_' + time.strftime("%Y_%m_%d_%H_%M_%S",
                                                                    time.localtime(time_start)) + ".csv"
    f = open(company_log_file, "w+", encoding='utf-8')
    for item in company_log_list:
        f.write(item)
    f.close()

    # print("=>WRITE log.txt FILE")
    log_list.append("=>写log结束 %s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_end))))
    f = open(log_file, "a", encoding='utf-8')
    for item in log_list:
        f.write(item)
    f.close()

    # print("=>WRITE loss_rate.csv FILE")
    f = open(loss_rate_file, "w", newline='', encoding='utf-8')
    writer = csv.writer(f)
    for item in loss_rate_list:
        writer.writerow(item)
    f.close()

    # print("=>WRITE time_delay.csv FILE")
    f = open(time_delay_file, "w", newline='', encoding='utf-8')
    writer = csv.writer(f)
    for item in time_delay_list:
        writer.writerow(item)
    f.close()


def count_test(self, max_n):
    print("开始休眠")
    for i in range(0, 100):
        # print(i)
        self.lb_m.insert(END, str(i))
        self.tv.step(1)
        time.sleep(1)
    print("休眠结束")


def sleep_test(self):
    max_n = 100
    t_c = threading.Thread(target=count_test, args=(self, max_n))
    t_c.start()


class App:
    def __init__(self, root):
        # 用三个LabelFrame将TopView分为三个区
        # 部区域
        group_top = LabelFrame(root, text="INPUT", padx=5, pady=5)
        group_top.grid(row=0, column=0, sticky=W)
        Label(group_top, text="City：").grid(row=0, column=0, sticky=W, padx=10, pady=5)
        Label(group_top, text="Company：").grid(row=1, column=0, sticky=W, padx=10, pady=5)
        Label(group_top, text="Thread：").grid(row=2, column=0, sticky=W, padx=10, pady=5)
        Button(group_top, text="Run", width=10, command=self.app_run).grid(row=3, column=0, sticky=W, padx=10, pady=5)
        Button(group_top, text="Sop", width=10, command=self.stop).grid(row=3, column=1, sticky=E, padx=10, pady=5)
        Button(group_top, text="Exit", width=10, command=root.quit).grid(row=3, column=2, sticky=W, padx=10, pady=5)

        v1 = StringVar(group_top, value="北京")
        v2 = StringVar(group_top, value="中国信息通信研究院")
        self.e1 = Entry(group_top, text=v1, validate="focusout", width=31)
        self.e2 = Entry(group_top, text=v2, validate="focusout", width=31)
        comvalue = StringVar()
        self.c_tread = ttk.Combobox(group_top, textvariable=comvalue, width=10)
        self.c_tread["values"] = ("33", "11", "1")
        self.c_tread.current(1)

        self.e1.grid(row=0, column=1, sticky=W, padx=10, pady=5)
        self.e2.grid(row=1, column=1, sticky=W, padx=10, pady=5)
        self.c_tread.grid(row=2, column=1, sticky=W, padx=10, pady=5)

        # 中部区域
        group_middle = LabelFrame(root, text="OUTPUT", padx=5, pady=5)
        group_middle.grid(row=1, column=0, sticky=W)

        sb_m = Scrollbar(group_middle)
        sb_m.pack(side=RIGHT, fill=Y)
        self.lb_m = Listbox(group_middle, yscrollcommand=sb_m.set, width=60, height=25)
        self.lb_m.pack(side=LEFT, fill=BOTH)
        sb_m.config(command=self.lb_m.yview)

        # 底部区域
        group_bottom = LabelFrame(root, text="MANAGER", padx=5, pady=5)
        group_bottom.grid(row=3, column=0, sticky=W)

        Button(group_bottom, text="IP_List_Test", width=10, command=self.ip_test).grid(row=0, column=0, sticky=W, padx=10, pady=5)
        Button(group_bottom, text="Report", width=10, command=self.report).grid(row=0, column=1, sticky=E, padx=10, pady=5)

        # 显示进度条
        self.tv = ttk.Progressbar(root, orient='horizontal', length=455, mode='determinate', value=0)
        self.tv.grid(row=2, column=0, sticky=W)

    def app_run(self):
        # print("City: %s " % self.e1.get())
        # print("Company: %s" % self.e2.get())
        # print("Thread: %s" % self.c_tread.get())
        self.lb_m.insert(END, "International Network Speed Tools")
        city = self.e1.get()
        company = self.e2.get()
        thread = self.c_tread.get()
        str_inert_city = "城市:"+city
        self.lb_m.insert(END, str_inert_city)
        str_inert_company = "公司:"+company
        self.lb_m.insert(END, str_inert_company)
        myaddr = socket.gethostbyname(socket.gethostname())
        str_insert_ip = "本次测试本地IP地址："+myaddr
        self.lb_m.insert(END, str_insert_ip)
        sleep_test(self)

    def stop(self):
        pass

    def ip_test(self):
        print("you click", self.tv['value']/self.tv['maximum']*100, '%')
        self.tv.step(5)

    def report(self):
        pass


if __name__ == "__main__":
    # 创建一个top level的根窗口，并把他作为参数实例化APP对象
    root = tk.Tk()
    root.title("International Network Speed Tools-V4.0(By Wayne Yu)")
    root.minsize(400, 800)  # 设置最小尺寸
    app = App(root)
    # 开始主事件循环
    root.mainloop()



