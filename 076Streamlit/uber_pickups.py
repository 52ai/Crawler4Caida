# coding:utf-8
"""
create on Jan 24, 2022 By Wenyan YU

Function:

My first data web app using Streamlit

"""
import streamlit as st
import pandas as pd
import numpy as np


st.title('Uber Pickups')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')


@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(1000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!(using st.cahce)')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_value = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(hist_value)


st.subheader('Map of all pickups')
st.map(data)

hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filter_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filter_data)

st.write('Finish My first data Web APP Demo')
st.subheader('- - - - - -  - Everything with Streamlit- - - - - - - - - -')
st.markdown("### Markdown Demo")
st.markdown("##### GoCN 每日新闻（2022-01-04）\n"\
               "1. [「GoCN 酷 Go 推荐」go 语言位操作库 — bitset](https://mp.weixin.qq.com/s/UcuKgKnt4fwrg3c-UHc3sw) \n"\
               "2. [Go 通过 Map/Filter/ForEach 等流式 API 高效处理数据](https://mp.weixin.qq.com/s/7ATm_Zu7ib9MXf8ugy3RcA)\n" \
               "3. [优化 Go 二进制文件的大小](https://prog.world/optimizing-the-size-of-the-go-binary)\n" \
               "4. [通常是无符号](https://graphitemaster.github.io/aau)\n"\
               "5. [将 Go 程序编译为 Nintendo Switch™ 的本机二进制文件](https://ebiten.org/blog/native_compiling_for_nintendo_switch.html)\n" \
               "- 编辑: CDS\n" \
               "- 订阅新闻: http://tinyletter.com/gocn\n" \
               "- 招聘专区: https://gocn.vip/jobs\n" \
               "- GoCN 归档: https://gocn.vip/topics/20927")

