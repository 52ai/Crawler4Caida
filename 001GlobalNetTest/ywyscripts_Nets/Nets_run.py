# coding:utf-8
"""
create on Oct 13, 2020 by Wenyan YU
Function:
国际互联网数据专用通道测速软件全面升级
版本V6：主要在V5版本基础之上，优化软件启动方式、新增定制化报告输出功能

输入：国际监测点信息，raw_data_excel.xlsx
输出: 测试结果，以excel的形式存储

"""
from tkinter import *
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import subprocess
import threading
import time
import re
import csv

import requests
import pandas as pd
from ipdb import City

ip_info = []  # 读取excel表存储

# lose_rate_list 用于存储丢包率，格式为country,ip,company1,company2,...,average
loss_rate_list = []
loss_rate_file = './loss_rate.csv'
# time_delay_list 用于存储时延，格式为country,ip,company1,company2,...,average
time_delay_list = []
time_delay_file = './time_delay.csv'

# log_list 用于存储所有log输出
log_list = []
log_file = './log.txt'

# company_log_list 用于存储每个企业测试输出日志数据，用于备份使用
company_log_list = []
# 全局的拆分后的IP地址列表
ip_info_threading = []


def get_ip_info(ip):
    """
    根据IPDB库，查询IP地址详细信息
    :param ip:
    :return ip_return:
    """
    db = City("mydata4vipday2_cn.ipdb")
    try:
        ip_return = db.find(ip, "CN")
    except Exception as e:
        print(e)
        ip_return = "查无"
    return ip_return


def run_ping_group(self, run_index):
    # print("run_index:", run_index)
    for run_item in ip_info_threading[run_index]:
        # print(run_item)
        # loss_rate, time_delay = run_ping(run_item[1])
        ftp_sub = subprocess.Popen("ping %s -n %d" % (run_item[1], self.n_ping),
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
        log_str = "%s, %s, %s, %s" % (run_item[0], run_item[1], loss_rate, time_delay.strip("ms"))
        company_log_list.append(log_str + "\n")
        # print(log_str)
        str_seq = str(run_index*self.max_ip_cnt + self.run_index_group[run_index])
        if len(str_seq) == 1:
            str_seq = "0"+str_seq
        group_finish_str = "已完成测试序号：" + str_seq
        print(".", end='')  # CMD终端输出
        self.lb_m.insert(END, group_finish_str)  # UI界面输出
        loss_rate_list[run_index * self.max_ip_cnt + self.run_index_group[run_index]].append(loss_rate)  # 添加丢包率
        time_delay_list[run_index * self.max_ip_cnt + self.run_index_group[run_index]].append(time_delay.strip("ms"))  # 添加时延
        self.run_index_group[run_index] += 1  # 组内索引自增1


def main_run(self):
    # 读丢包率存储文件
    f_loss_rate = open(loss_rate_file, "r", encoding='gbk')
    for line in f_loss_rate.readlines():
        # print(line.strip().split(','))
        loss_rate_list.append(line.strip().split(','))
    f_loss_rate.close()
    # print(loss_rate_list)

    # 读时延存储文件
    # print("=>read time_delay file, generate time_delay_list")
    f_time_delay = open(time_delay_file, "r", encoding='gbk')
    for line in f_time_delay.readlines():
        # print(line.strip().split(','))
        time_delay_list.append(line.strip().split(','))
    f_loss_rate.close()
    # print(time_delay_list)

    # 开始测试
    time_start = time.time()
    start_str = "=>TEST START:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_start))
    print(start_str)  # CMD终端输出
    self.lb_m.insert(END, start_str)  # UI界面输出

    # 下面开始读取IP地址列表进行ping测试，设置并发线程个数为n_threading
    tmp_ip_info = []
    item_index = 1
    for item in ip_info:
        if item_index % self.max_ip_cnt != 0:
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
    #     loss_rate, time_delay = run_ping_group(item[1])
    #     log_str = "%s, %s, %s, %s" % (item[0], item[1], loss_rate, time_delay)
    #     company_log_list.append(log_str + "\n")
    #     print(log_str)
    #     loss_rate_list[item_index].append(loss_rate)  # 添加丢包率
    #     time_delay_list[item_index].append(time_delay)  # 添加时延
    #     item_index += 1  # 索引自增1
    # # print(len(ip_info))

    # 读取拆分后的IP地址列表，分别生成PING的测试线程，以组为单位
    threads = []  # 存储进程
    item_index = 0
    for item in ip_info_threading:
        # print(item)
        threads.append(threading.Thread(target=run_ping_group, args=(self, item_index,)))
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
    time_consuming = float('%.2f' % (time_end - time_start))
    end_str = "=>TEST FINISH:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_end)) + ", TIME CONSUMING：" + str(time_consuming) + "s"
    print(end_str)  # CMD终端输出
    self.lb_m.insert(END, end_str)  # UI终端输出
    self.lb_m.insert(END, self.str_line)

    self.btn_run.configure(state='normal')  # 设置Run 按钮为可用
    self.btn_stop.configure(state='normal')  # 设置Stop 按钮为可用
    self.btn_exit.configure(state='normal')  # 设置Exit 按钮为可用

    # 写企业日志文件
    company_log_str = "%s, %s, %s, %s" % ("-", "-", "-", "-")
    company_log_list.append(company_log_str + "\n")
    company_log_str = "%s, %s, %s, %s" % (self.e1.get(), self.e2.get(), str(self.ip_isp), str(self.ip_public))
    company_log_list.append(company_log_str + "\n")

    # print("=>WRITE company_log")
    company_log_file = './result/company_log_' + time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time_start)) + ".csv"
    f = open(company_log_file, "w+", encoding='gbk')
    for item in company_log_list:
        f.write(item)
    f.close()
    company_log_list.clear()  # 清空企业日志列表

    # 写CMD终端日志输出文件
    # print("=>WRITE log.txt FILE")
    log_list.append("=>写log结束 %s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_end))))
    f = open(log_file, "a", encoding='utf-8')
    for item in log_list:
        f.write(item)
    f.close()
    log_list.clear()  # 清空日志存储文件，继续下一轮测试

    # 写丢包率存储文件
    # print("=>WRITE loss_rate.csv FILE")
    f = open(loss_rate_file, "w", newline='', encoding='gbk')
    writer = csv.writer(f)
    for item in loss_rate_list:
        writer.writerow(item)
    f.close()
    loss_rate_list.clear()  # 清空丢包率存储列表

    # 写时延存储文件
    # print("=>WRITE time_delay.csv FILE")
    f = open(time_delay_file, "w", newline='', encoding='gbk')
    writer = csv.writer(f)
    for item in time_delay_list:
        writer.writerow(item)
    f.close()
    time_delay_list.clear()  # 清空时延存储列表

    ip_info_threading.clear()  # 清空全局的多线程IP列表


def ip_test_run_thread(self, run_item):
    # print(run_item)
    # loss_rate, time_delay = run_ping(run_item[1])
    ftp_sub = subprocess.Popen("ping %s -n 4" % run_item[1],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    ret = ftp_sub.stdout.read()
    str_ret = ret.decode('gbk')
    try:
        loss_rate = re.findall('\d+%', str_ret)[0]
        time_delay = re.findall('\d+ms', str_ret)[-1]

    except IndexError:
        str_invalid_country = "=>" + run_item[0]
        # print(str_invalid_country)
        self.lb_m.insert(END, str_invalid_country)


def ip_test_run(self):
    # 读IP地址列表，分别生成PING的测试线程
    threads_ip_test = []  # 存储进程
    for item in ip_info:
        threads_ip_test.append(threading.Thread(target=ip_test_run_thread, args=(self, item,)))
    for t in threads_ip_test:
        t.setDaemon(True)
        t.start()
    # 必须等待for循环里面的所有线程都结束后，再执行主线程
    for k in threads_ip_test:
        k.join()
    self.btn_ip_test.configure(state='normal')
    self.lb_m.insert(END, self.str_line)
    tk.messagebox.showinfo("提示", "一键测试IP列表结束，请替换失效的IP地址！")


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
        # 设置参数
        self.n_threading = 11  # 设置默认并发线程数为11次
        # 根据并发发线程数，拆分IP地址列表，按照等分，每轮的个数为IP列表总的个数除以并发数，向上取整
        self.max_ip_cnt = (len(ip_info) // self.n_threading)
        self.run_index_group = [0] * self.n_threading  # 存储组内坐标列表，初始化全为0

        self.str_line = "------------------------------"

        self.n_ping = 10  # 设置每次ping发送的数据包个数，默认为10

        # 获取公网IP地址
        req = requests.get("http://txt.go.sohu.com/ip/soip")
        self.ip_public = re.findall('\d+.\d+.\d+.\d+', req.text)[0]
        self.ip_isp = "查无"  # 获取运营商信息

        # 用三个LabelFrame将TopView分为三个区
        # 部区域
        group_top = LabelFrame(root, text="INPUT", padx=5, pady=5)
        group_top.grid(row=0, column=0, sticky=W)
        Label(group_top, text="City：").grid(row=0, column=0, sticky=W, padx=10, pady=5)
        Label(group_top, text="Company：").grid(row=1, column=0, sticky=W, padx=10, pady=5)
        Label(group_top, text="Thread：").grid(row=2, column=0, sticky=W, padx=10, pady=5)
        Label(group_top, text="Ping：").grid(row=3, column=0, sticky=W, padx=10, pady=5)

        self.btn_run = Button(group_top, text="Run", width=10, command=self.app_run)
        self.btn_run.grid(row=4, column=0, sticky=W, padx=10, pady=5)
        self.btn_stop = Button(group_top, text="Sop", width=10, command=self.stop)
        self.btn_stop.grid(row=4, column=1, sticky=E, padx=10, pady=5)
        self.btn_exit = Button(group_top, text="Exit", width=10, command=self.sys_exit)
        self.btn_exit.grid(row=4, column=2, sticky=W, padx=10, pady=5)

        v1 = StringVar(group_top, value="北京")
        v2 = StringVar(group_top, value="中国信息通信研究院")
        self.e1 = Entry(group_top, text=v1, validate="focusout", width=31)
        self.e2 = Entry(group_top, text=v2, validate="focusout", width=31)
        comvalue_thread = StringVar()
        self.c_thread = ttk.Combobox(group_top, textvariable=comvalue_thread, width=10)
        self.c_thread["values"] = ("33", "11", "1")
        self.c_thread.current(1)

        comvalue_ping = StringVar()
        self.c_ping = ttk.Combobox(group_top, textvariable=comvalue_ping, width=10)
        self.c_ping["values"] = ("1", "10", "50", "100", "200")
        self.c_ping.current(1)

        self.e1.grid(row=0, column=1, sticky=W, padx=10, pady=5)
        self.e2.grid(row=1, column=1, sticky=W, padx=10, pady=5)
        self.c_thread.grid(row=2, column=1, sticky=W, padx=10, pady=5)
        self.c_ping.grid(row=3, column=1, sticky=W, padx=10, pady=5)

        # print(self.c_thread.get())
        # print(self.c_ping.get())

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

        self.btn_ip_test = Button(group_bottom, text="IP_List_Test", width=10, command=self.ip_test)
        self.btn_ip_test.grid(row=0, column=0, sticky=W, padx=10, pady=5)
        self.btn_report = Button(group_bottom, text="Report", width=10, command=self.report)
        self.btn_report.grid(row=0, column=1, sticky=E, padx=10, pady=5)

        # 显示进度条
        self.tv = ttk.Progressbar(root, orient='horizontal', length=455, mode='determinate', value=0)
        self.tv.grid(row=2, column=0, sticky=W)

    def app_run(self):
        if len(self.c_thread.get()) == 0 or len(self.c_ping.get()) == 0 or len(self.e1.get()) == 0 or len(self.e2.get()) == 0 :
            tk.messagebox.showinfo("提示", "参数设置不可为空，请设置好全部参数，再运行测试程序！")
            return
        # self.c_thread.current(1)
        # self.c_ping.current(3)
        # print("City: %s " % self.e1.get())
        # print("Company: %s" % self.e2.get())
        # print("Thread: %s" % self.c_thread.get())
        # print(self.c_thread.get())
        # print(self.c_ping.get())
        self.lb_m.insert(END, "International Network Speed Tools")
        city = self.e1.get()
        company = self.e2.get()
        thread = self.c_thread.get()
        str_insert_city = "城市："+city
        self.lb_m.insert(END, str_insert_city)
        str_insert_company = "公司："+company
        self.lb_m.insert(END, str_insert_company)
        str_insert_ip = "本次测试公网IP地址：" + self.ip_public
        self.lb_m.insert(END, str_insert_ip)
        self.ip_isp = get_ip_info(self.ip_public)[4]
        str_insert_isp = "所属运营商：" + self.ip_isp
        self.lb_m.insert(END, str_insert_isp)
        # sleep_test(self)

        # 根据UI参数选择，更新测试的参数
        str_n_threading = "本次测试线程数：" + self.c_thread.get()
        self.n_threading = int(self.c_thread.get())
        self.lb_m.insert(END, str_n_threading)

        str_n_ping = "每个IP发送数据包的个数：" + self.c_ping.get()
        self.n_ping = int(self.c_ping.get())
        self.lb_m.insert(END, str_n_ping)

        self.max_ip_cnt = (len(ip_info) // self.n_threading)
        self.run_index_group = [0] * self.n_threading  # 存储组内坐标列表，初始化全为0
        # print(self.max_ip_cnt)
        # print(self.run_index_group)
        self.lb_m.insert(END, self.str_line)

        # 开始测速
        t_main_run = threading.Thread(target=main_run, args=(self,))
        t_main_run.start()
        # 把run按钮设为不可用
        self.btn_run.configure(state='disabled')
        self.btn_stop.configure(state='disabled')
        self.btn_run.configure(state='disabled')
        self.btn_exit.configure(state='disabled')

    def stop(self):
        tk.messagebox.showinfo("提示", "此功能待开发，其必要性需进一步讨论！")

    def sys_exit(self):
        root.quit()

    def ip_test(self):
        self.lb_m.insert(END, "International Network Speed Tools")
        self.lb_m.insert(END, "一键测试IP列表，失效的IP地址如下（请更换对应国家的IP地址）：")
        self.btn_ip_test.configure(state='disabled')
        # 开始一键测试IP列表
        t_main_run = threading.Thread(target=ip_test_run, args=(self,))
        t_main_run.start()

    def report(self):
        tk.messagebox.showinfo("提示", "需根据个性化需求定制报表生成功能！")


def read_ip_info(file_path):
    """
    读取ip info excel信息
    :param file_path:
    :return:
    """
    data = pd.read_excel(file_path)
    # print(data['监测点名称'])
    # print(data['IP'])
    ip_info_dic = {}
    for i in range(0,len(data['监测点名称'])):
        # print(data["监测点名称"][i].split("_")[0])
        location = data["监测点名称"][i].split("_")[0]
        if location not in ip_info_dic:
            ip_info_dic[location] = data["IP"][i]
        else:
            pass
    # print(ip_info_dic)
    temp_list = []
    for key in ip_info_dic:
        # print(key, ip_info_dic[key])
        temp_list.append(key)
        temp_list.append(ip_info_dic[key])
        ip_info.append(temp_list)
        temp_list = []
    # print(len(ip_info))
    return ip_info


if __name__ == "__main__":
    # 读取ip_info
    ip_info_excel_path = "./raw_data_excel.xlsx"
    ip_info = read_ip_info(ip_info_excel_path)
    # print(ip_info)
    # 创建一个top level的根窗口，并把他作为参数实例化APP对象
    root = tk.Tk()
    root.title("Nets Tools-V6.0(By Wenyan YU)")
    root.minsize(400, 800)  # 设置最小尺寸
    app = App(root)
    # 开始主事件循环
    root.mainloop()




