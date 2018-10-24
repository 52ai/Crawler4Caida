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


def run_ping_test(ip_str):
    """
    进行一组ping的测试，每组n次
    :return:str_ret
    """
    # list_p_r = []
    ftp_sub = subprocess.Popen("ping %s -n 10" % ip_str,
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    ret = ftp_sub.stdout.read()
    str_ret = ret.decode('gbk')
    print(str_ret)
    print(re.findall('\d+%', str_ret)[0])
    print(re.findall('\d+ms', str_ret)[-1])


if __name__ == "__main__":
    # 例：中亚-哈萨克斯坦/95.56.234.66
    ip_str = "95.56.234.66"
    run_ping_test(ip_str)