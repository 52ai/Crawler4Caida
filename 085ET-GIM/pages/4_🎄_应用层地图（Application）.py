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
    page_title="应用层地图",
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
    menu = ["默认", "全球", "中国", "美国", "德国", "俄罗斯", "日本"]
    port_list = ["53", "80", "443"]
    map_style_list = ["mapbox://styles/mapbox/dark-v10",
                      "mapbox://styles/mapbox/light-v10",
                      "mapbox://styles/mapbox/streets-v11",
                      "mapbox://styles/mapbox/satellite-v9",
                      "dark",
                      "light",
                      "dark_no_labels",
                      "light_no_labels",
                      ]
    st.sidebar.markdown(" ")
    choice = st.sidebar.selectbox("请选择目标国家或地区：", menu)
    port_value = st.sidebar.selectbox("请选择开放端口:", port_list)
    map_style = st.sidebar.selectbox("地图样式：", map_style_list)
    with st.expander("全球网络应用层地图绘制（更多参数设置）", False):
        map_point_radius = st.number_input("地图节点大小：", value=1, min_value=0, max_value=10)
        map_point_color = st.color_picker("地图节点颜色：", "#EC7E22")
        map_line_width = st.number_input("地图连边粗细：", value=2, min_value=0, max_value=10)
        is_heatmap_mode = st.radio("选择是否开启热力图模式:", (True, False))
        is_hexagon_mode = st.radio("选择是否开启Hexagon模式：", (False, True))

    def hex_to_rgb(h):
        h = h.lstrip("#")
        return tuple(int(h[i: i + 2], 16) for i in (0, 2, 4))

    port_geo_file = "../000LocalData/IPPorts/map_" + port_value + ".csv"
    # port_geo_file = "../000LocalData/IPPorts/map_53.csv"

    if choice != "默认":
        st.write("地图绘制时间:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "\n")

        st.write("当前选择的绘图范围:", choice)
        st.write("当前选择的开放端口:", port_value)
        st.write("正在努力加载全球端口扫描数据...")
        # print(port_geo_file)
        port_geo_list = []  # 存储端口的定位及相关信息
        except_info_cnt = 0  # 统计存在定位信息缺失的数据
        with open(port_geo_file, 'r', encoding="gbk") as f:
            flag_float = 0.0
            all_line = 0  # 统计全球总的节点数量
            current_area_cnt = 0  # 统计当前绘图范围的节点数量
            for line in f.readlines():
                line = line.strip().split(",")
                all_line += 1
                # print(line)
                temp_dic = dict().copy()
                try:
                    if len(line) == 4:
                        temp_dic["country"] = line[0]
                    else:
                        temp_dic["country"] = line[1]
                    if choice == "全球" or choice == temp_dic["country"]:
                        current_area_cnt += 1  # 当前绘图范围的节点数量自增1
                        temp_dic["org"] = line[-3]
                        temp_dic["coordinates"] = [float(line[-1]), float(line[-2])]
                        # print(temp_dic)
                        current_float = temp_dic["coordinates"][0]+temp_dic["coordinates"][1]
                        if current_float != flag_float:
                            # print(current_float, flag_float)
                            port_geo_list.append(temp_dic)
                            flag_float = (temp_dic["coordinates"][0]+temp_dic["coordinates"][1])
                        del temp_dic
                except Exception as e:
                    except_info_cnt += 1


        with open("port_geo_53.json", 'w') as f_obj:
            json.dump(port_geo_list, f_obj)

        layer_scatter_ip = pdk.Layer(
            "ScatterplotLayer",
            port_geo_list,
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

        layer_heatmap_ip = pdk.Layer(
            "HeatmapLayer",
            port_geo_list if is_heatmap_mode else [],
            opacity=0.9,
            get_position="coordinates")

        layer_hexagon_ip = pdk.Layer(
            'HexagonLayer',  # `type` positional argument is here, CPUGridLayer, HexagonLayer,GridLayer
            port_geo_list if is_hexagon_mode else [],
            get_position="coordinates",
            auto_highlight=True,
            elevation_scale=1000,
            pickable=True,
            elevation_range=[40, 1000],
            extruded=True,
            coverage=1,
            radius=100, )

        # Set the viewport location
        view_state = pdk.ViewState(
            longitude=0,
            latitude=9,
            zoom=2,
            min_zoom=2,
            max_zoom=22,
            pitch=45,
            bearing=0)
        # Combined all of it and render a viewport
        r = pdk.Deck(map_style=map_style,
                     layers=[layer_heatmap_ip, layer_scatter_ip, layer_hexagon_ip],
                     initial_view_state=view_state,
                     tooltip={
                         # 'html': '<b>Elevation Value:</b> {elevationValue}',
                         'text': '国家：{country}\n公司：{org}\n地理坐标:{coordinates}',
                         'style': {
                             'color': 'white'
                         },
                     }
                     )
        st.pydeck_chart(r)
        r.to_html("Global_demo.html")

        st.write("全球扫描出的开放端口数量:", all_line)
        st.write("当前绘图范围的节点数量:", current_area_cnt)
        st.write("实际绘图节点数量（排除多IP重合定位，降低GIS地图渲染负载）:", len(port_geo_list))
        # with st.expander("详细列表", False):
        #     st.json(port_geo_list)
        st.write("缺失地理位置信息的节点数量", except_info_cnt)
    else:
        st.image("./image/dns53_map.PNG", caption="图例：全球DNS基础设施分布图（2022）")
        st.write("深度整合开源GIS地图系统，依托全球开放端口扫描数据，绘制全球各国应用层地图")
        st.write("因应用层所需的全球端口扫描数据过于庞大，地图渲染时间相对比较长，故默认不做渲染。")
        st.write("请在左侧选择绘图范围，开始绘图！")
else:
    st.info("请先点击首页下拉选择框，登录系统！")
