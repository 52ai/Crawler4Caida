import pandas as pd
import streamlit as st
import time
import numpy as np
import json

from st_card import st_card
import pydeck as pdk
from pydeck.types import String
import graphviz as graphviz

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import Div
from bokeh.palettes import Spectral
from bokeh.plotting import figure
import math

from functools import reduce

st.set_page_config(
    page_title="逻辑层地图",
    page_icon="world_map",
    layout="wide",
)

# 去除streamlit的原生标记
sys_menu = '''
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
'''
st.markdown(sys_menu, unsafe_allow_html=True)

if 'count' not in st.session_state:
    st.session_state.count = 0
    st.session_state.user = "Guest"

# 给侧边栏添加APP版本信息
with st.sidebar:
    st.write("Login:", st.session_state.user)
    st.sidebar.markdown(
        """
        <small> ET-GIM 0.1.0 | Jane 2022 </small>  
        [<img src='http://www.mryu.top/content/templates/start/images/github.png' class='img-fluid' width=25 height=25>](https://github.com/52ai) 
        [<img src='http://www.mryu.top/content/templates/start/images/weibo.png' class='img-fluid' width=25 height=25>](http://weibo.com/billcode) 
         """,
        unsafe_allow_html=True,
    )


if st.session_state.count > 0:
    menu = ["中国", "美国", "德国", "俄罗斯", "日本", "全球"]
    map_style_list = ["mapbox://styles/mapbox/dark-v10",
                      "mapbox://styles/mapbox/light-v10",
                      "mapbox://styles/mapbox/streets-v11",
                      "mapbox://styles/mapbox/satellite-v9",
                      "dark",
                      "light",
                      "dark_no_labels",
                      "light_no_labels",
                      ]
    aim_as_list = ["4134", "4837", "9808",
                   "6939", "7018", "15169",
                   "12389",
                   "3320",
                   "4713"]  # 存储需要分析的as列表

    st.sidebar.markdown(" ")
    choice = st.sidebar.selectbox("请选择目标国家或地区：", menu)
    map_style = st.sidebar.selectbox("地图样式：", map_style_list)
    map_point_radius = st.sidebar.number_input("地图节点大小：", value=1, min_value=0, max_value=10)
    map_point_color = st.sidebar.color_picker("地图节点颜色：", "#DEC512")
    map_line_width = st.sidebar.number_input("地图连边粗细：", value=2, min_value=0, max_value=10)
    is_heatmap_mode = st.sidebar.radio("选择是否开启热力图模式:", (True, False))
    is_hexagon_mode = st.sidebar.radio("选择是否开启Hexagon模式：", (False, True))
    is_circle_mode = st.sidebar.radio("选择是否开启GreateCircle模式：", (False, True))
    aim_as_value = st.sidebar.selectbox("请选择需要目标自治域网络:", aim_as_list)


    def hex_to_rgb(h):
        h = h.lstrip("#")
        return tuple(int(h[i: i + 2], 16) for i in (0, 2, 4))


    COLOR_BREWER_BLUE_SCALE = [
        [240, 249, 232],
        [204, 235, 197],
        [168, 221, 181],
        [123, 204, 196],
        [67, 162, 202],
        [8, 104, 172]]

    asns_geo_file = "./map_logical/asns_geo_all.csv"
    as_rel_file = "./map_logical/20220701.as-rel.txt"

    country2ab = {"中国": "CN",
                  "美国": "US",
                  "德国": "DE",
                  "俄罗斯": "RU",
                  "日本": "JP"}

    st.write("深度整合开源GIS地图系统，在全球互联网络拓扑研究基础上，绘制全球各国逻辑层地图")
    st.write("地图绘制时间:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "\n")
    st.write("当前选择的绘图范围:", choice)
    as_geo_list = []  # 存储全球as地理定位数据
    except_info_list = []  # 统计存在地理定位缺失的数据
    area_as_geo_dic = {}  # 存储as的经纬度
    with open(asns_geo_file, 'r', encoding="utf-8") as f:
        all_line = 0  # 存储自治域网络画像数量
        current_area_cnt = 0  # 统计当前绘图范围的节点数量
        for line in f.readlines():
            all_line += 1
            line = line.strip().split(",")
            temp_dic = dict().copy()
            if len(line) == 6:
                long = float(line[3])
                lat = float(line[4])
                as_info = "AS" + line[0] + "," + line[1]
                temp_dic["name"] = as_info
                temp_dic["country"] = line[2]
                temp_dic["source"] = line[-1]
                temp_dic["coordinates"] = [long, lat]
                if choice == "全球" or country2ab[choice] == temp_dic["country"]:
                    as_geo_list.append(temp_dic)
                    current_area_cnt += 1
                    area_as_geo_dic[line[0]] = [long, lat]
                del temp_dic
            else:
                except_info_list.append(line[0])

    # 生成互联关系数据
    rel_geo_list = []  # 存储互联关系对
    rel_all_cnt = 0  # 存储采集到的全部互联关系数量
    rel_area_draw = 0  # 存储有效绘图关系数量
    with open(as_rel_file, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if line.find("#") != -1:
                continue
            rel_all_cnt += 1
            line = line.strip().split("|")
            # print(line)
            left_as = line[0]
            right_as = line[1]
            rel_type = line[2]
            temp_dic = dict().copy()
            if left_as == aim_as_value or right_as == aim_as_value:
                if left_as in area_as_geo_dic.keys() and right_as in area_as_geo_dic.keys():
                    temp_dic["name"] = "AS" + left_as + "- AS" + right_as
                    temp_dic["type"] = rel_type
                    temp_dic["from"] = area_as_geo_dic[left_as]
                    temp_dic["to"] = area_as_geo_dic[right_as]
                    rel_geo_list.append(temp_dic)
                    rel_area_draw += 1
                    del temp_dic

    layer_scatter_as = pdk.Layer(
        "ScatterplotLayer",
        as_geo_list,
        pickable=True,  # 可选择
        opacity=0.8,  # 透明度
        stroked=True,  # 绘制点的轮廓
        filled=True,  # 绘制点的填充区
        radius_scale=6,  # 所有点的全局半径乘数
        radius_min_pixels=map_point_radius,  # 点半径的最小值
        radius_max_pixels=100,  # 点半径的最大值
        line_width_min_pixels=0.5,  # 线的最小的像素值
        get_position="coordinates",  # 获取位置信息
        # get_fill_color=[255, 140, 0],  # 填充的颜色
        get_fill_color=hex_to_rgb(map_point_color),
        get_line_color=[0, 0, 0])

    layer_heatmap_as = pdk.Layer(
        "HeatmapLayer",
        as_geo_list if is_heatmap_mode else [],
        opacity=0.9,
        get_position="coordinates",
        # color_range=COLOR_BREWER_BLUE_SCALE,
        pickable=True,)

    layer_hexagon_as = pdk.Layer(
        'HexagonLayer',  # `type` positional argument is here, CPUGridLayer, HexagonLayer,GridLayer
        as_geo_list if is_hexagon_mode else [],
        get_position="coordinates",
        auto_highlight=True,
        elevation_scale=1000,
        pickable=True,
        elevation_range=[40, 1000],
        extruded=True,
        coverage=1,
        radius=100, )

    layer_circle_as = pdk.Layer(
        "GreatCircleLayer",
        rel_geo_list if is_circle_mode else [],
        pickable=True,
        get_stroke_width=12,
        width_min_pixels=map_line_width,
        get_source_position="from",
        get_target_position="to",
        get_source_color=[64, 255, 0],
        get_target_color=[0, 128, 200],
        auto_highlight=True,
    )

    # Set the viewport location
    view_state = pdk.ViewState(
        longitude=116,
        latitude=39,
        zoom=3,
        min_zoom=1,
        max_zoom=22,
        pitch=0,
        bearing=0)
    # Combined all of it and render a viewport
    r = pdk.Deck(map_style=map_style,
                 layers=[layer_heatmap_as, layer_scatter_as, layer_hexagon_as, layer_circle_as],
                 initial_view_state=view_state,
                 tooltip={
                     # 'html': '<b>Elevation Value:</b> {elevationValue}',
                     'text': 'Info：{name}\n国家：{country}\n来源：{source}\n地理坐标:{coordinates}',
                     'style': {
                         'color': 'white'
                     },
                 }
                 )
    st.pydeck_chart(r)

    st.write("已收集全球自治域网络画像数量:", all_line)
    st.write("已处理有效地理定位信息的数量", len(as_geo_list))
    with st.expander("详细列表", False):
        st.json(as_geo_list)
    st.write("当前绘图范围实际节点数量（约等于已分配ASN数量）:", current_area_cnt)
    st.write("已收集全球自治域互联关系数量:", rel_all_cnt)
    st.write("当前绘图有效网络互联关系数量:", rel_area_draw)


else:
    st.info("请先点击首页下拉选择框，登录系统！")
