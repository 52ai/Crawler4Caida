import psutil
import streamlit as st
import time
import datetime
from streamlit_autorefresh import st_autorefresh
from streamlit_apex_charts import bar_chart, pie_chart
import pandas as pd
import platform
import os


st.set_page_config(page_title="系统信息查看器", page_icon="💻", layout="wide")

st_autorefresh(interval=5000, limit=100000, key="Mr.R")

st.header("系统信息查看器")
base_infor = [[datetime.datetime.now().strftime("%Y-%m-%d %H: %M: %S"), str(psutil.users()[0][0]), platform.platform()]]
df_base_infor = pd.DataFrame(base_infor, columns=["当前时间", "登陆者", "操作系统"])
st.table(df_base_infor)


#获取网卡名称
def get_key():
    key_info = psutil.net_io_counters(pernic=True).keys()  # 获取网卡名称
    recv = {}
    sent = {}
    for key in key_info:
        recv.setdefault(key, psutil.net_io_counters(pernic=True).get(key).bytes_recv)  # 各网卡接收的字节数
        sent.setdefault(key, psutil.net_io_counters(pernic=True).get(key).bytes_sent)  # 各网卡发送的字节数
    return key_info, recv, sent


#获取网卡速率
def get_rate(func):
    key_info, old_recv, old_sent = func()  # 上一秒收集的数据
    time.sleep(1)
    key_info, now_recv, now_sent = func()  # 当前所收集的数据
    net_in = {}
    net_out = {}
    for key in key_info:
        net_in.setdefault(key, (now_recv.get(key) - old_recv.get(key)) / 1024)  # 每秒接收速率
        net_out.setdefault(key, (now_sent.get(key) - old_sent.get(key)) / 1024)  # 每秒发送速率
    return key_info, net_in, net_out


c1, c2, c3 = st.columns(3)

with c1:
    #内存
    mem = psutil.virtual_memory()
    zj = float(mem.total) / 1024 / 1024 / 1024
    ysy = float(mem.used) / 1024 / 1024 / 1024
    kx = float(mem.free) / 1024 / 1024 / 1024

    data_neicun = [[round(ysy,2),round(kx, 2)]]
    df_neicun = pd.DataFrame(data_neicun, columns=["已用内存","空闲内存"])
    pie_chart("内存使用情况(GB)", df_neicun)


    #CPU
    cpu_liyonglv = (str(psutil.cpu_percent(1))) + '%'
    cpu_data = [[cpu_liyonglv]]
    df_cpu = pd.DataFrame(cpu_data, columns=["CPU利用率"])
    bar_chart("CPU利用率(%)", df_cpu)

with c2:
    #磁盘
    dk = psutil.disk_usage('/')
    total = dk.total / 1024 / 1024 / 1024
    used = dk.used / 1024 / 1024 / 1024
    free = dk.free / 1024 / 1024 / 1024

    cipan_shiyong = [[used, free]]
    df_cipan = pd.DataFrame(cipan_shiyong, columns=["已使用磁盘大小","空闲磁盘大小"])
    pie_chart("磁盘使用率(%)", df_cipan)

    #网络速率
    key_info, net_in, net_out = get_rate(get_key)
    wangka_liuliang = []
    for key in key_info:
             wangka_liuliang.append([net_in.get(key),net_out.get(key)])
    speed_internet = wangka_liuliang
    df_speed = pd.DataFrame(speed_internet, columns=["下行速率","上行速率"])
    bar_chart("网络速率(kb/s)", df_speed)



with c3:
    #进程信息
    pids = psutil.pids()
    process = []
    for pid in pids:
        p = psutil.Process(pid)
        process_name = p.name()
        process.append([pid, process_name, p.is_running()])

    df_process = pd.DataFrame(process, columns=["PID","进程名","是否还在运行"])
    st.dataframe(df_process)

    #已安装软件
    # import wmi
    # c = wmi.WMI()
    # software_list = []
    # for s in c.Win32_Product():
    #     software_list.append([s.Caption, s.Vendor, s.Version])
    # if len(software_list)>1:
    #     st.dataframe(pd.DataFrame(software_list, columns=["名称","发布人","版本"]))
    # else:
    #     st.info("正在导出已安装的软件程序列表")