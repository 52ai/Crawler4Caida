# coding:utf-8
"""
create on Oct 26,2018 by Wayne Yu
Version : 2.0
Function:
该程序旨在对工业园区的出国网速进行测试，并按一定的格式输出报告。
以国家（IP地址）为单位，通过ping和tracert命令去统计丢包率、时延以及经过的路由表。
例：中亚-哈萨克斯坦/95.56.234.66

由于所属区域划分不明确，因此以国家为单位进行测试，后续再进行区域的划分。
输出分成三个文件（即两个list，一份CMD log），每次测试一个企业就读一个文件（记list）然后在后面添加测试的数据。
lose_rate.csv
time_delay.csv
log.txt

通过这三个文件进行数据的记录和整理。每个文件存储的内容如下：

lose_rate.csv
country, ip, company1, company2,……，average

time_delay.csv
country, ip, company1, company2,……，average

log.txt
所有的cmd输出都保存在这个log.txt里面，以企业为单位，测试先后顺序进行存储。

"""
import subprocess
import threading
import time
import re

# ip_info 用于存储需要测试IP地址及其地理信息
ip_info = [["新加坡", "180.210.206.51"],
           ["马来西亚", "223.25.244.145"],
           ["越南", "45.117.76.22"],
           ["泰国", "43.254.132.221"],
           ["澳大利亚", "203.143.89.72"],
           ["印度", "49.50.76.218"],
           ["阿联酋", "185.93.245.54"],
           ["土耳其", "185.125.32.29"],
           ["沙特", "46.151.213.205"],
           ["哈萨克斯坦", "95.56.234.66"],
           ["蒙古", "43.231.113.234"],
           ["日本", "45.32.51.106"],
           ["韩国", "103.86.86.82"],
           ["香港", "203.160.84.241"],
           ["台湾", "113.196.70.31"],
           ["英国", "5.1.88.152"],
           ["德国", "185.72.247.76"],
           ["荷兰", "81.171.7.115"],
           ["俄罗斯", "46.38.51.201"],
           ["乌克兰", "91.229.78.83"],
           ["意大利", "185.94.16.23"],
           ["葡萄牙", "188.208.143.109"],
           ["芬兰", "185.87.108.247"],
           ["埃及", "41.215.240.197"],
           ["肯尼亚", "62.12.114.67"],
           ["尼日利亚", "154.113.1.27"],
           ["南非", "41.185.78.52"],
           ["美国", "204.188.217.238"],
           ["加拿大", "198.50.128.225"],
           ["墨西哥", "143.255.57.123"],
           ["巴西", "181.41.214.27"],
           ["阿根廷", "200.55.240.23"],
           ["智利", "190.105.239.70"]]


def run_ping_test(ip_str):
    """
    进行一组ping的测试，每组n次
    :return:loss_rate, time_delay
    """
    # list_p_r = []
    # print("本组测试开始(", ip_str, ")：ping %s -n 3 ", ip_str)
    ftp_sub = subprocess.Popen("ping %s -n 3" % ip_str,
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    ret = ftp_sub.stdout.read()
    str_ret = ret.decode('gbk')
    # print(str_ret)
    # print("本组测试丢包率(", ip_str, ")：", re.findall('\d+%', str_ret)[0])
    # print("本组测试平均时延(", ip_str, ")：", re.findall('\d+ms', str_ret)[-1])
    try:
        loss_rate = re.findall('\d+%', str_ret)[0]
        time_delay = re.findall('\d+ms', str_ret)[-1]
    except IndexError:
        loss_rate = "NONE"
        time_delay = "INFINITE"
    return loss_rate, time_delay


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
    time_start = time.time()
    print("测试启动:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_start)))
    for item in ip_info:
        # print(item)
        loss_rate, time_delay = run_ping_test(item[1])
        print(item[0], ":丢包率(%s)  平均时延（%s）" % (loss_rate, time_delay))
    # print(len(ip_info))
    time_end = time.time()
    print("测试结束:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_end)), "，共耗时：", (time_end - time_start), "s")