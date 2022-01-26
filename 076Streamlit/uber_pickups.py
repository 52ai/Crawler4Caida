# coding:utf-8
"""
create on Jan 24, 2022 By Wenyan YU

Function:

My first data web app using Streamlit

"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import datetime
from PIL import Image
import time
from streamlit_option_menu import option_menu

st.set_page_config(
     page_title="MachineEyes",
     page_icon="http://www.mryu.top/yun.ico",
     layout="centered",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'http://www.mryu.top/',
         'Report a bug': "http://www.mryu.top/",
         'About': "Eyes of the Machine Senses Everything of Network."
     }
 )

with st.sidebar:
    selected = option_menu(
        "",
        ["48hours", "Monthly", "Archive", 'Visualization', 'User'],
        icons=['alarm', 'calendar2-month', "list-task", 'graph-up-arrow', 'heart'],
        menu_icon="cast",
        default_index=1)

st.write("You select %s Menu" % selected)

if selected == '48hours':
    str_markdown = "##### GoCN 每日新闻（2022-01-04）\n" \
                   "1. [「GoCN 酷 Go 推荐」go 语言位操作库 — bitset](https://mp.weixin.qq.com/s/UcuKgKnt4fwrg3c-UHc3sw) \n" \
                   "2. [Go 通过 Map/Filter/ForEach 等流式 API 高效处理数据](https://mp.weixin.qq.com/s/7ATm_Zu7ib9MXf8ugy3RcA)\n" \
                   "3. [优化 Go 二进制文件的大小](https://prog.world/optimizing-the-size-of-the-go-binary)\n" \
                   "4. [通常是无符号](https://graphitemaster.github.io/aau)\n" \
                   "5. [将 Go 程序编译为 Nintendo Switch™ 的本机二进制文件](https://ebiten.org/blog/native_compiling_for_nintendo_switch.html)\n" \
                   "- 编辑: CDS\n" \
                   "- 订阅新闻: http://tinyletter.com/gocn\n" \
                   "- 招聘专区: https://gocn.vip/jobs\n" \
                   "- GoCN 归档: https://gocn.vip/topics/20927"

    st.markdown(str_markdown)
elif selected == "User":
    pass
else:
    pass
