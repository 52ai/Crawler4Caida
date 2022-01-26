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
        "MachineEyes",
        ["实时舆情", "每日舆情", "每月舆情", '事件分析', '用户登录'],
        icons=['house', 'cloud-upload', "list-task", 'gear', 'file-earmark-person'],
        menu_icon="cast",
        default_index=1)

st.write("You select %s Vertical Menu" % selected)
