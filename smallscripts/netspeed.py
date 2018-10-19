# coding:utf-8
"""
create on Oct 19, 2018 by Wayne Yu

"""
# import os
#
# ip = "127.0.0.1"
# print(os.system('ping ' + ip))

import subprocess
import threading
import time
import re
#
# ip_num = 256
# list_ping_result = []
#
#
# class PingThread(threading.Thread):
#
#     def __init__(self, str_ip, sleep_time, g_list_p_r):
#         threading.Thread.__init__(self)
#         self.sleep_time = sleep_time
#         self.str_ip = str_ip
#         self.list_p_r = g_list_p_r
#
#     def run(self):
#         time.sleep(self.sleep_time)
#         ftp_sub = subprocess.Popen("ping %s -n 3" % self.str_ip,
#                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
#         ret = ftp_sub.stdout.read()
#         str_ret = ret.decode("gbk")
#         ret_s = re.search("TTL", str_ret)
#         if ret_s:
#             self.list_p_r.append(('ping    ok', self.str_ip))
#         else:
#             self.list_p_r.append(('ping error', self.str_ip))
#
#
# def cmp_s(toupe_str):
#     str_val = toupe_str[1]
#     ret_group = re.match("\d*", str_val[::-1])
#     str_ret = ret_group.group()
#     return int(str_ret[::-1])
#
#
# thread_id = []
# for i in range(ip_num):
#     thread_id.append(0)
#     thread_id[i] = PingThread("192.168.8.%d" % i, int(i / 20), list_ping_result)
#     thread_id[i].start()
#     print(i, end='')
#
# while True:
#     if len(list_ping_result) >= ip_num:
#         list_ping_result.sort(key=cmp_s)
#         for i in list_ping_result:
#             print(i)
#
#         break


def run(ip):
    list_p_r = []
    ftp_sub = subprocess.Popen("ping %s -n 5" % ip,
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    ret = ftp_sub.stdout.read()
    str_ret = ret.decode("gbk")
    print(str_ret)
    ret_s = re.search("TTL", str_ret)
    if ret_s:
       list_p_r.append(('ping ok', ip))
    else:
        list_p_r.append(('ping error', ip))
    return list_p_r


ip = "45.32.51.106"
print(run(ip))
