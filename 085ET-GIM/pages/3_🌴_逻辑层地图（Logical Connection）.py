import pandas as pd
import streamlit as st
import time
import numpy as np
import json
import random

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
        <small> Driven By PYTHON </small>
        """,
        unsafe_allow_html=True,
    )


if st.session_state.count > 0:
    menu = ["美国", "中国", "德国", "俄罗斯", "日本", "全球"]
    map_style_list = ["mapbox://styles/mapbox/dark-v10",
                      "mapbox://styles/mapbox/light-v10",
                      "mapbox://styles/mapbox/streets-v11",
                      "mapbox://styles/mapbox/satellite-v9",
                      "dark",
                      "light",
                      "dark_no_labels",
                      "light_no_labels",
                      ]
    aim_as_list = ["默认", "4134", "4837", "9808",
                   "6939", "7018", "15169",
                   "12389",
                   "3320",
                   "4713"]  # 存储需要分析的as列表

    st.sidebar.markdown(" ")

    choice = st.sidebar.selectbox("请选择目标国家或地区：", menu)
    map_style = st.sidebar.selectbox("地图样式：", map_style_list)

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

    as_geo_list = []  # 存储全球as地理定位数据
    except_info_list = []  # 统计存在地理定位缺失的数据
    area_as_geo_dic = {}  # 存储as的经纬度
    global_as_geo_dic = {}  # 存储全球as经纬度
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
                global_as_geo_dic[line[0]] = [long, lat]  # 存储全球as geo 信息，给路由导航使用
            else:
                except_info_list.append(line[0])
    # print(as_geo_list[0:4])
    search_list = [item['name']+","+item['source'] for item in as_geo_list]
    # print(search_list[0:4])
    search_all_list = ["默认"]
    search_all_list.extend(search_list)

    with st.expander("全球网络逻辑层地图绘制（更多参数设置）", False):
        map_point_radius = st.number_input("地图节点大小：", value=1, min_value=0, max_value=10)
        map_point_color = st.color_picker("地图节点颜色：", "#DEC512")
        map_line_width = st.number_input("地图连边粗细：", value=4, min_value=0, max_value=10)
        is_heatmap_mode = st.radio("选择是否开启热力图模式:", (True, False))
        is_hexagon_mode = st.radio("选择是否开启Hexagon模式：", (False, True))
        is_circle_mode = st.radio("选择是否开启GreateCircle模式：", (False, True))
        aim_as_value = st.selectbox("请选择需要绘制GreateCircle的目标自治域网络:", aim_as_list)

    search_value = st.sidebar.selectbox("请搜索目标自治域网络:", search_all_list)
    print(search_value)
    cols0, cols1, cols2 = st.sidebar.columns([1, 1, 1])
    with cols0:
        is_route_mode = st.radio("选择是否开启路由导航模式:", (False, True))
    with cols1:
        from_as_value = st.selectbox("选择出发网络(FROM-AS):", ["4134", "4837", "9808"])
    with cols2:
        to_as_value = st.selectbox("选择到达网络(TO-AS):", ["27064", "15169", "3356", "7018", "2516", "9605", "397942"])

    search_as_geo_list = []
    view_longitude = -100
    view_latitude = 39
    view_zoom = 3

    # 获取目标自治域网络的经纬度信息
    for item in as_geo_list:
        if search_value == (item['name']+","+item['source']):
            search_as_geo_list.append(item)
            view_longitude = item['coordinates'][0]
            view_latitude = item['coordinates'][1]

    # print(search_as_geo_list)

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

    # 生成路由导航数据（根据FROM-AS以及TO-AS的值，匹配路由表中的多路径，然后根据路径最短原则，选择最优路由）
    # 若已开启了路由导航模式，则处理AS PATH数据
    as_line_map = []  # 存储as line数据
    if is_route_mode:
        rib_file = "./data/z20220320.txt"
        rib_as_path_list = []  # 存储路由表中有效的as path
        with open(rib_file, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip().split("|")
                as_path = line[-2].split(" ")
                last_as = as_path[-1]
                if as_path[-1].find("{") != -1:
                    last_as = as_path[-1].strip("{").strip("}").split(",")[0]
                first_as = as_path[0]
                if last_as == to_as_value and first_as == from_as_value:
                    # print("FROM:", first_as, "TO:", last_as, "\nAS PATH:", as_path)
                    if as_path not in rib_as_path_list:
                        rib_as_path_list.append(as_path)
        print("有效路径:", len(rib_as_path_list), rib_as_path_list)

        # 根据有效路径，生成地图绘制的路线图数据
        path_id = 1  # 存储路径的编号
        item_dict = {}
        for line in rib_as_path_list:
            item_dict_temp = item_dict.copy()
            item_dict_temp["id"] = path_id
            item_dict_temp["name"] = "第" + str(path_id) + "条路:" + str(line)
            item_dict_temp["path_length"] = len(line)
            # 随机生成颜色数组
            # color_list = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            color_list = (34, 139, 34)
            item_dict_temp["color"] = color_list
            path = []  # 存储线段的经纬度信息
            for as_item in line:
                as_geo = global_as_geo_dic[as_item]
                path.append(as_geo)
            item_dict_temp["path"] = path
            as_line_map.append(item_dict_temp)
            del item_dict_temp
            path_id += 1  # 路径的编号自增1

        print(as_line_map)
        # 根据路径最短优先原则，取最优路径
        as_line_map_best = []
        best_id = 0
        shortest_path = 10  # 设置最长路径为10
        for item_id in range(0, len(as_line_map)):
            print(item_id)
            if as_line_map[item_id]["path_length"] < shortest_path:
                best_id = item_id
        as_line_map_best.append(as_line_map[best_id])
        print(as_line_map_best)

    cols0, cols1, cols2, cols3, cols4 = st.columns([1, 1, 1, 1, 1])
    with cols0:
        st_card('All ASN', value=all_line, unit='', show_progress=False)
    with cols1:
        st_card('Deal Geo ASN', value=len(as_geo_list), unit='', show_progress=False)
    with cols2:
        st_card('Draw ASN', value=current_area_cnt, unit='', show_progress=False)
    with cols3:
        st_card('All REL Info', value=rel_all_cnt, unit='', show_progress=False)
    with cols4:
        st_card('Draw REL', value=rel_area_draw, unit='', show_progress=False)

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

    layer_scatter_as_search = pdk.Layer(
        "ScatterplotLayer",
        search_as_geo_list,
        pickable=True,  # 可选择
        opacity=1,  # 透明度
        stroked=True,  # 绘制点的轮廓
        filled=True,  # 绘制点的填充区
        radius_scale=6,  # 所有点的全局半径乘数
        radius_min_pixels=4,  # 点半径的最小值
        radius_max_pixels=100,  # 点半径的最大值
        line_width_min_pixels=0.5,  # 线的最小的像素值
        get_position="coordinates",  # 获取位置信息
        # get_fill_color=[255, 140, 0],  # 填充的颜色
        get_fill_color=hex_to_rgb('#F10F46'),
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

    layer_path_route = pdk.Layer(
        type="PathLayer",
        data=as_line_map_best if is_route_mode else [],
        pickable=True,
        get_color="color",
        width_scale=20,
        width_min_pixels=map_line_width,
        get_path="path",
        get_width=5,
    )

    # Set the viewport location
    if search_value == "默认":
        view_state = pdk.ViewState(
            longitude=-100,
            latitude=39,
            zoom=3,
            min_zoom=1,
            max_zoom=22,
            pitch=0,
            bearing=0)
    else:
        view_state = pdk.ViewState(
            longitude=view_longitude,
            latitude=view_latitude,
            zoom=view_zoom,
            min_zoom=1,
            max_zoom=22,
            pitch=0,
            bearing=0)

    # Combined all of it and render a viewport
    r = pdk.Deck(map_style=map_style,
                 layers=[layer_heatmap_as,
                         layer_scatter_as,
                         layer_hexagon_as,
                         layer_circle_as,
                         layer_scatter_as_search,
                         layer_path_route],
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
    r.to_html("us_as_demo.html")

    st.write("深度整合开源GIS地图系统，在全球互联网络拓扑研究基础上，绘制全球各国逻辑层地图")
    st.write("地图绘制时间:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "\n")
    st.write("当前选择的绘图范围:", choice)

    # st.write("已收集全球自治域网络画像数量:", all_line)
    # st.write("已处理有效地理定位信息的数量", len(as_geo_list))
    # # with st.expander("详细列表", False):
    # #     st.json(as_geo_list)
    # st.write("当前绘图范围实际节点数量（约等于已分配ASN数量）:", current_area_cnt)
    # st.write("已收集全球自治域互联关系数量:", rel_all_cnt)
    # st.write("当前绘图有效网络互联关系数量:", rel_area_draw)

else:
    st.info("请先点击首页下拉选择框，登录系统！")
