# coding:utf-8
"""
create on Oct 23,2018 by Wayne Yu
Function:
该程序旨在对工业园区的出国网速进行测试，并按一定的格式输出报告。
以国家（IP地址）为单位，通过ping和tracert命令去统计丢包率、时延以及经过的路由表。
例：中亚-哈萨克斯坦/95.56.234.66
"""
import subprocess
import threading
import time
import re

# ip_info 用于存储需要测试IP地址及其地理信息
ip_info = [["中亚-哈萨克斯坦", "95.56.234.66"],
           ["中亚-吉尔吉斯斯坦-比什凯克", "91.213.233.234"],
           ["西亚-蒙古-乌兰巴托", "43.231.113.234"],
           ["西亚-伊朗-德黑兰", "130.185.78.165"],
           ["西亚-阿联酋-迪拜", "185.93.245.54"],
           ["西亚-土耳其-伊斯坦布尔", "185.125.32.29"],
           ["西亚-沙特阿拉伯-利雅得", "46.151.213.205"],
           ["南亚-印度-新德里", "49.50.76.218"],
           ["东南亚-印度尼西亚-雅加达", "103.65.236.189"],
           ["东南亚-越南-胡志明", "45.117.76.22"],
           ["东南亚-新加坡", "180.210.206.51"],
           ["东南亚-泰国-曼谷", "43.254.132.221"],
           ["日本-东京", "45.32.51.106"],
           ["台北", "113.196.70.31"],
           ["香港", "203.160.84.241"],
           ["欧洲-乌克兰-哈尔科夫", "91.229.78.83"],
           ["欧洲-意大利-米兰", "185.94.16.23"],
           ["欧洲-俄罗斯-莫斯科", "46.38.51.201"],
           ["欧洲-德国-法兰克福", "185.72.247.76"],
           ["欧洲-英国-伦敦", "5.1.88.152"],
           ["美洲-美国-芝加哥", "204.188.217.238"],
           ["美洲-美国-纽约", "12.0.1.28"],
           ["美洲-加拿大-多伦多", "198.50.128.225"],
           ["美洲-阿根廷-布宜诺斯艾利斯", "200.55.240.23"],
           ["大洋洲-澳大利亚-悉尼", "203.143.89.72"],
           ["大洋洲-新西兰-奥克兰", "49.50.255.132"]]


def run_ping_test(ip_str):
    """
    进行一组ping的测试，每组n次
    :return:loss_rate, time_delay
    """
    # list_p_r = []
    # print("本组测试开始(", ip_str, ")：ping %s -n 3 ", ip_str)
    ftp_sub = subprocess.Popen("ping %s -n 5" % ip_str,
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
    print("测试启动:", time_start)
    for item in ip_info:
        # print(item)
        loss_rate, time_delay = run_ping_test(item[1])
        print(item[0], ":丢包率(%s)  平均时延（%s）" % (loss_rate, time_delay))
    time_end = time.time()
    print("测试结束:", time_end, "，共耗时：", (time_end - time_start), "ms")
"""
在windows下使用tracert 命令得到的原输出如下：
通过最多 30 个跃点跟踪
到 vps-1149050-3181.cp.idhost.kz [95.56.234.66] 的路由:
  1     *        *        *     请求超时。
  2     2 ms     2 ms     1 ms  10.6.1.181 
    ....
 28   294 ms   295 ms   301 ms  vps-1149050-3181.cp.idhost.kz [95.56.234.66] 
跟踪完成。
"""