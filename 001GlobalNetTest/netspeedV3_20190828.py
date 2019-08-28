# coding:utf-8
"""
create on Oct 26,2018 by Wayne Yu
Version : 3.0

该脚本程序在V2.0的基础之上增加了并发的功能，以缩短测试的时间（以33个国际IP地址为例，每个地址ping 50次，需耗时大概50分钟）。
为尽可能的减少并发ping带来的时延和丢包率的影响，并发的线程数要尽可能的少（控制在10个线程以内）
并发之后程序的结构，需要进行调整

20190828 更新了测试的国际IP地址
"""
import subprocess
import threading
import time
import re
import csv

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
        ftp_sub = subprocess.Popen("ping %s -n 50" % run_item[1],
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


def run_tracert_test(ip_str):
    """
    进行一次tracert命令，输出经过的路由
    :param ip_str:
    :return: tracert_list
    """
    ftp_sub = subprocess.Popen("tracert %s" % ip_str,
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    ret = ftp_sub.stdout.read()
    str_ret = ret.decode('gbk')
    print(str_ret)
    print(re.findall("\d+\.\d+\.\d+\.\d+", str_ret))  # 提取所有经过的路由IP地址


if __name__ == "__main__":
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
    print("=>TEST FINISH:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_end)), ", TIME CONSUMING：", (time_end - time_start), "s")

    # print("=>WRITE company_log")
    company_log_file = 'C:/ywyscripts/company_log_' + time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time_start)) + ".csv"
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
"""
33国际IP，ping 50，33个并发，进行实验
=>TEST FINISH: 2018-10-30 18:13:51 , TIME CONSUMING： 86.72197484970093 s
33国际IP，ping 50，11个并发，进行实验
=>TEST FINISH: 2018-10-30 18:26:23 , TIME CONSUMING： 180.65175580978394 s
33国际IP，ping 500,11个并发，进行实验
=>TEST FINISH: 2018-10-31 10:49:59 , TIME CONSUMING： 2194.2702968120575 s
33国际IP，ping 300,11个并发，进行实验
=>TEST START: 2018-10-31 12:23:05
.................................All threading finished!
=>TEST FINISH: 2018-10-31 12:30:33 , TIME CONSUMING： 447.999125957489 s
"""


