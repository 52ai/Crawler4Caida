import streamlit as st
import streamlit.components.v1 as components
import json, requests
from datetime import date, timedelta

st.set_page_config(page_title="我的天气查询平台", page_icon="☔", layout="wide")

st.sidebar.header("天气查询平台")

choose = st.sidebar.radio("",("天气预报","天气实况","综合数据"))

#隐藏网页右上角和正下方的链接
sysmenu = '''
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
'''
st.markdown(sysmenu,unsafe_allow_html=True)

#调整sidebar宽度
st.sidebar.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 200px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 200px;
        margin-left: -250px;
    }
    </style>
    """,
    unsafe_allow_html=True,)


if choose == "天气预报":
    c1, c2, c3 = st.columns([0.35,3,2.2])
    with c1:
        st.empty()
    with c2:
        components.iframe("http://data.cma.cn/forecast/index.html?t=54511", width=1400,height=1040)
    with c3:
        st.empty()
elif choose == "天气实况":
    c1, c2, c3 = st.columns([0.35,3,2.2])
    with c1:
        st.empty()
    with c2:
        components.iframe("https://data.cma.cn/data/online/t/1", width=1400,height=1040)
    with c3:
        st.empty()
elif choose == "综合数据":
    c1, c2, c3 = st.columns([0.35,3,2.2])
    with c1:
        st.empty()
    with c2:
        components.iframe("https://data.cma.cn/dataGis/gis.html", width=1400,height=1040)
    with c3:
        st.empty()


def set_page_container_style(max_width, max_width_100_percent,padding_top, padding_right, padding_left, padding_bottom,color, background_color
    ):
        if max_width_100_percent:
            max_width_str = f'max-width: 100%;'
        else:
            max_width_str = f'max-width: {max_width}px;'
        st.markdown(
            f'''
            <style>
                .reportview-container .sidebar-content {{
                    padding-top: {padding_top}rem;
                }}
                .reportview-container .main .block-container {{
                    {max_width_str}
                    padding-top: {padding_top}rem;
                    padding-right: {padding_right}rem;
                    padding-left: {padding_left}rem;
                    padding-bottom: {padding_bottom}rem;
                }}
                .reportview-container .main {{
                    color: {color};
                    background-color: {background_color};
                }}
            </style>
            ''',
            unsafe_allow_html=True,
        )

#设置页面背景及其他参数
set_page_container_style(80, True, 0.5, 1, 0.1, 1, "#1aff1a", "#1aa3ff")

#第二种来源
st.sidebar.header("明日天气预报")
city = st.sidebar.text_input("请输入你要查询的城市名称", value="北京")

weatherJsonUrl = "http://wthrcdn.etouch.cn/weather_mini?city="+str(city)  # 将链接定义为一个字符串
response = requests.get(weatherJsonUrl)  # 获取并下载页面，其内容会保存在respons.text成员变量里面
response.raise_for_status()  # 这句代码的意思如果请求失败的话就会抛出异常，请求正常就上面也不会做

# 将json文件格式导入成python的格式
weatherData = json.loads(response.text)
#st.write(weatherData)

tomorrow = (date.today() + timedelta(days= 1)).strftime("%Y-%m-%d")
weather_dict = dict()
weather_dict['high'] = weatherData['data']['forecast'][0]['high']
weather_dict['low'] = weatherData['data']['forecast'][0]['low']
weather_dict['type'] = weatherData['data']['forecast'][0]['type']
weather_dict['fengxiang'] = weatherData['data']['forecast'][0]['fengxiang']
weather_dict['ganmao'] = weatherData['data']['ganmao']

st.sidebar.write("Hi,明天是"+tomorrow, "，"+str(city)+"的室外温度🌡️在"+weather_dict['low'][2:]+"~"+weather_dict['high'][2:]+
    "之间。会有"+weather_dict['type']+"和"+weather_dict['fengxiang']+"🍃出现。"+weather_dict['ganmao'])