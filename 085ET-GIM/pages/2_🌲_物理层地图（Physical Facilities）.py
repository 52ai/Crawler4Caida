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


st.set_page_config(
    page_title="物理层地图",
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
    menu = ["全球", "中国", "美国", "德国", "俄罗斯", "日本", "中国台湾"]
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
    map_style = st.sidebar.selectbox("地图样式：", map_style_list)
    map_point_radius = st.sidebar.number_input("地图节点大小：", value=2, min_value=0, max_value=10)
    map_point_color = st.sidebar.color_picker("地图节点颜色：", "#11EAD8")
    map_line_width = st.sidebar.number_input("地图连边粗细：", value=3, min_value=0, max_value=10)
    is_single_cable_mode = st.sidebar.radio("请选择是否进入海缆Single模式:", (False, True))
    is_heatmap_mode = st.sidebar.radio("选择是否开启热力图模式:", (False, True))
    is_hexagon_mode = st.sidebar.radio("选择是否开启Hexagon模式：", (False, True))

    def hex_to_rgb(h):
        h = h.lstrip("#")
        return tuple(int(h[i: i + 2], 16) for i in (0, 2, 4))


    landing_point = './map_physical/cable_v3/landing-point-geo.json'
    cable_line = './map_physical/cable_v3/cable-geo.json'

    if choice == "全球":
        cable_list = []  # 存储全球所有海缆
        with open(cable_line, 'r', encoding='utf-8') as cable_line_f:
            cable_line_dic = json.load(cable_line_f)
            for item in cable_line_dic["features"]:
                cl_dic = item["properties"]
                cable_list.append(cl_dic["name"])
        cable_list.sort(reverse=False)

        single_cable_name = st.selectbox("请选择或搜索需要了解的海缆（需开启Single模式）:", cable_list)
        st.markdown("深度整合开源GIS地图系统，构建全球各国物理层地图绘制（Submarine Cables Map）")
        st.write("地图绘制时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "\n")

        landing_point_map = []  # 存储海缆登陆站字典列表
        with open(landing_point, 'r', encoding='utf-8') as landing_point_f:
            landing_point_dic = json.load(landing_point_f)
            for item in landing_point_dic["features"]:
                lp_dic = item["properties"]
                lp_dic["coordinates"] = item["geometry"]["coordinates"]
                landing_point_map.append(lp_dic)

        cable_line_map = []  # 存储海缆路由字典列表
        cable_line_map_all = []  # 许多海缆成鱼骨状，需要形成多条记录
        with open(cable_line, 'r', encoding='utf-8') as cable_line_f:
            cable_line_dic = json.load(cable_line_f)
            for item in cable_line_dic["features"]:
                cl_dic = item["properties"]
                cl_dic["color"] = hex_to_rgb(cl_dic["color"])
                cable_line_map.append(cl_dic)
                for multi_path in item["geometry"]["coordinates"]:
                    cl_dic_temp = cl_dic.copy()  # 创建新独立字典
                    # print("multi_path", multi_path)
                    cl_dic_temp["path"] = multi_path
                    if is_single_cable_mode:
                        if cl_dic_temp["name"] == single_cable_name:
                            cable_line_map_all.append(cl_dic_temp)
                    else:
                        cable_line_map_all.append(cl_dic_temp)

                    del cl_dic_temp  # 销毁该字典

        print(cable_line_map_all[0:3])

        layer_scatter_lp = pdk.Layer(
            "ScatterplotLayer",
            landing_point_map,
            pickable=True,  # 可选择
            opacity=0.8,  # 透明度
            stroked=True,  # 绘制点的轮廓
            filled=True,  # 绘制点的填充区
            radius_scale=6,  # 所有点的全局半径乘数
            radius_min_pixels=map_point_radius,  # 点半径的最小值
            radius_max_pixels=100,  # 点半径的最大值
            line_width_min_pixels=1,  # 线的最小的像素值
            get_position="coordinates",  # 获取位置信息
            # get_fill_color=[255, 140, 0],  # 填充的颜色
            get_fill_color=hex_to_rgb(map_point_color),
            get_line_color=[0, 0, 0])

        layer_heatmap_lp = pdk.Layer(
            "HeatmapLayer",
            landing_point_map if is_heatmap_mode else [],
            opacity=0.9,
            get_position="coordinates")

        layer_hexagon_lp = pdk.Layer(
            'HexagonLayer',  # `type` positional argument is here, CPUGridLayer, HexagonLayer,GridLayer
            landing_point_map if is_hexagon_mode else [],
            get_position="coordinates",
            auto_highlight=True,
            elevation_scale=100,
            pickable=True,
            elevation_range=[10, 3000],
            extruded=True,
            coverage=1,
            radius=10,)

        layer_path_cable = pdk.Layer(
            type="PathLayer",
            data=cable_line_map_all,
            pickable=True,
            get_color="color",
            width_scale=20,
            width_min_pixels=map_line_width,
            get_path="path",
            get_width=5,
        )

        # Set the viewport location
        view_state = pdk.ViewState(
            longitude=0,
            latitude=23.26,
            zoom=2,
            min_zoom=0,
            max_zoom=22,
            pitch=0,
            bearing=0)
        # Combined all of it and render a viewport
        r = pdk.Deck(map_style=map_style,
                     layers=[layer_hexagon_lp, layer_heatmap_lp, layer_path_cable, layer_scatter_lp],
                     initial_view_state=view_state,
                     tooltip={
                         # 'html': '<b>Elevation Value:</b> {elevationValue}',
                         'text': '名称：{name}\n地理坐标:{coordinates}',
                         'style': {
                             'color': 'white'
                         },
                     }
                     )
        st.pydeck_chart(r)
        st.write("全球海底光缆数量：", len(cable_line_map))
        with st.expander("详细列表", False):
            st.json(cable_line_map)

        st.write("全球海缆登陆站数量：", len(landing_point_map))
        with st.expander("详细列表", False):
            st.json(landing_point_map)
        # st.write("全球海底光缆多路径绘图统计（条）:", len(cable_line_map_all))

    elif choice == "中国":
        country_cable_file = "./map_physical/cable_v3/country/china.json"
        cable_list_country = []  # 存储该国所有海缆
        with open(country_cable_file, 'r', encoding='utf-8') as f:
            country_cable_dic = json.load(f)
            for item in country_cable_dic["cables"]:
                cable_list_country.append(item)
        is_planed_list = [item for item in cable_list_country if item["is_planned"]]
        is_used_list = [item for item in cable_list_country if not item["is_planned"]]
        cable_name_list = [item["name"] for item in cable_list_country]
        single_cable_name = st.selectbox("请选择或搜索需要了解的海缆（需开启Single模式）:", cable_name_list)

        st.write("深度整合开源GIS地图系统，构建全球各国物理层地图绘制（Submarine Cables Map）— ", choice)
        st.write("地图绘制时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "\n")

        landing_point_map = []  # 存储海缆登陆站字典列表
        with open(landing_point, 'r', encoding='utf-8') as landing_point_f:
            landing_point_dic = json.load(landing_point_f)
            for item in landing_point_dic["features"]:
                lp_dic = item["properties"]
                lp_dic["coordinates"] = item["geometry"]["coordinates"]
                landing_point_map.append(lp_dic)

        cable_line_map = []  # 存储海缆路由字典列表
        cable_line_map_all = []  # 许多海缆成鱼骨状，需要形成多条记录
        with open(cable_line, 'r', encoding='utf-8') as cable_line_f:
            cable_line_dic = json.load(cable_line_f)
            for item in cable_line_dic["features"]:
                cl_dic = item["properties"]
                cl_dic["color"] = hex_to_rgb(cl_dic["color"])
                cable_line_map.append(cl_dic)
                for multi_path in item["geometry"]["coordinates"]:
                    cl_dic_temp = cl_dic.copy()  # 创建新独立字典
                    # print("multi_path", multi_path)
                    cl_dic_temp["path"] = multi_path
                    if is_single_cable_mode:
                        if cl_dic_temp["name"] == single_cable_name:
                            cable_line_map_all.append(cl_dic_temp)
                    else:
                        if cl_dic_temp["name"] in cable_name_list:
                            cable_line_map_all.append(cl_dic_temp)

                    del cl_dic_temp  # 销毁该字典

        layer_scatter_lp = pdk.Layer(
            "ScatterplotLayer",
            landing_point_map,
            pickable=True,  # 可选择
            opacity=0.8,  # 透明度
            stroked=True,  # 绘制点的轮廓
            filled=True,  # 绘制点的填充区
            radius_scale=6,  # 所有点的全局半径乘数
            radius_min_pixels=map_point_radius,  # 点半径的最小值
            radius_max_pixels=100,  # 点半径的最大值
            line_width_min_pixels=1,  # 线的最小的像素值
            get_position="coordinates",  # 获取位置信息
            # get_fill_color=[255, 140, 0],  # 填充的颜色
            get_fill_color=hex_to_rgb(map_point_color),
            get_line_color=[0, 0, 0])

        layer_heatmap_lp = pdk.Layer(
            "HeatmapLayer",
            landing_point_map if is_heatmap_mode else [],
            opacity=0.9,
            get_position="coordinates")

        layer_hexagon_lp = pdk.Layer(
            'HexagonLayer',  # `type` positional argument is here, CPUGridLayer, HexagonLayer,GridLayer
            landing_point_map if is_hexagon_mode else [],
            get_position="coordinates",
            auto_highlight=True,
            elevation_scale=100,
            pickable=True,
            elevation_range=[10, 3000],
            extruded=True,
            coverage=1,
            radius=10, )

        layer_path_cable = pdk.Layer(
            type="PathLayer",
            data=cable_line_map_all,
            pickable=True,
            get_color="color",
            width_scale=20,
            width_min_pixels=map_line_width,
            get_path="path",
            get_width=5,
        )

        # Set the viewport location
        view_state = pdk.ViewState(
            longitude=0,
            latitude=0,
            zoom=2,
            min_zoom=0,
            max_zoom=22,
            pitch=45,
            bearing=0)
        # Combined all of it and render a viewport
        r = pdk.Deck(map_style=map_style,
                     layers=[layer_hexagon_lp, layer_heatmap_lp, layer_path_cable, layer_scatter_lp],
                     initial_view_state=view_state,
                     tooltip={
                         # 'html': '<b>Elevation Value:</b> {elevationValue}',
                         'text': '{name}',
                         'style': {
                             'color': 'white'
                         },
                     }
                     )
        st.pydeck_chart(r)
        st.write("海缆数量总计：", len(cable_list_country))
        st.write("其中已投入使用的数量：", len(is_used_list))
        with st.expander("详细列表", False):
            st.json(is_used_list)
        st.write("正在建设中的数量:", len(is_planed_list))
        with st.expander("详细列表", False):
            st.json(is_planed_list)
    elif choice == "美国":
        country_cable_file = "./map_physical/cable_v3/country/united-states.json"
        cable_list_country = []  # 存储该国所有海缆
        with open(country_cable_file, 'r', encoding='utf-8') as f:
            country_cable_dic = json.load(f)
            for item in country_cable_dic["cables"]:
                cable_list_country.append(item)
        is_planed_list = [item for item in cable_list_country if item["is_planned"]]
        is_used_list = [item for item in cable_list_country if not item["is_planned"]]
        cable_name_list = [item["name"] for item in cable_list_country]
        single_cable_name = st.selectbox("请选择或搜索需要了解的海缆（需开启Single模式）:", cable_name_list)

        st.write("深度整合开源GIS地图系统，构建全球各国物理层地图绘制（Submarine Cables Map）— ", choice)
        st.write("地图绘制时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "\n")

        landing_point_map = []  # 存储海缆登陆站字典列表
        with open(landing_point, 'r', encoding='utf-8') as landing_point_f:
            landing_point_dic = json.load(landing_point_f)
            for item in landing_point_dic["features"]:
                lp_dic = item["properties"]
                lp_dic["coordinates"] = item["geometry"]["coordinates"]
                landing_point_map.append(lp_dic)

        cable_line_map = []  # 存储海缆路由字典列表
        cable_line_map_all = []  # 许多海缆成鱼骨状，需要形成多条记录
        with open(cable_line, 'r', encoding='utf-8') as cable_line_f:
            cable_line_dic = json.load(cable_line_f)
            for item in cable_line_dic["features"]:
                cl_dic = item["properties"]
                cl_dic["color"] = hex_to_rgb(cl_dic["color"])
                cable_line_map.append(cl_dic)
                for multi_path in item["geometry"]["coordinates"]:
                    cl_dic_temp = cl_dic.copy()  # 创建新独立字典
                    # print("multi_path", multi_path)
                    cl_dic_temp["path"] = multi_path
                    if is_single_cable_mode:
                        if cl_dic_temp["name"] == single_cable_name:
                            cable_line_map_all.append(cl_dic_temp)
                    else:
                        if cl_dic_temp["name"] in cable_name_list:
                            cable_line_map_all.append(cl_dic_temp)

                    del cl_dic_temp  # 销毁该字典

        layer_scatter_lp = pdk.Layer(
            "ScatterplotLayer",
            landing_point_map,
            pickable=True,  # 可选择
            opacity=0.8,  # 透明度
            stroked=True,  # 绘制点的轮廓
            filled=True,  # 绘制点的填充区
            radius_scale=6,  # 所有点的全局半径乘数
            radius_min_pixels=map_point_radius,  # 点半径的最小值
            radius_max_pixels=100,  # 点半径的最大值
            line_width_min_pixels=1,  # 线的最小的像素值
            get_position="coordinates",  # 获取位置信息
            # get_fill_color=[255, 140, 0],  # 填充的颜色
            get_fill_color=hex_to_rgb(map_point_color),
            get_line_color=[0, 0, 0])

        layer_heatmap_lp = pdk.Layer(
            "HeatmapLayer",
            landing_point_map if is_heatmap_mode else [],
            opacity=0.9,
            get_position="coordinates")

        layer_hexagon_lp = pdk.Layer(
            'HexagonLayer',  # `type` positional argument is here, CPUGridLayer, HexagonLayer,GridLayer
            landing_point_map if is_hexagon_mode else [],
            get_position="coordinates",
            auto_highlight=True,
            elevation_scale=100,
            pickable=True,
            elevation_range=[10, 3000],
            extruded=True,
            coverage=1,
            radius=10, )

        layer_path_cable = pdk.Layer(
            type="PathLayer",
            data=cable_line_map_all,
            pickable=True,
            get_color="color",
            width_scale=20,
            width_min_pixels=map_line_width,
            get_path="path",
            get_width=5,
        )

        # Set the viewport location
        view_state = pdk.ViewState(
            longitude=0,
            latitude=0,
            zoom=2,
            min_zoom=1,
            max_zoom=22,
            pitch=45,
            bearing=0)
        # Combined all of it and render a viewport
        r = pdk.Deck(map_style=map_style,
                     layers=[layer_hexagon_lp, layer_heatmap_lp, layer_path_cable, layer_scatter_lp],
                     initial_view_state=view_state,
                     tooltip={
                         # 'html': '<b>Elevation Value:</b> {elevationValue}',
                         'text': '{name}',
                         'style': {
                             'color': 'white'
                         },
                     }
                     )
        st.pydeck_chart(r)
        st.write("海缆数量总计：", len(cable_list_country))
        st.write("其中已投入使用的数量：", len(is_used_list))
        with st.expander("详细列表", False):
            st.json(is_used_list)
        st.write("正在建设中的数量:", len(is_planed_list))
        with st.expander("详细列表", False):
            st.json(is_planed_list)
    elif choice == "德国":
        country_cable_file = "./map_physical/cable_v3/country/germany.json"
        cable_list_country = []  # 存储该国所有海缆
        with open(country_cable_file, 'r', encoding='utf-8') as f:
            country_cable_dic = json.load(f)
            for item in country_cable_dic["cables"]:
                cable_list_country.append(item)
        is_planed_list = [item for item in cable_list_country if item["is_planned"]]
        is_used_list = [item for item in cable_list_country if not item["is_planned"]]
        cable_name_list = [item["name"] for item in cable_list_country]
        single_cable_name = st.selectbox("请选择或搜索需要了解的海缆（需开启Single模式）:", cable_name_list)

        st.write("深度整合开源GIS地图系统，构建全球各国物理层地图绘制（Submarine Cables Map）— ", choice)
        st.write("地图绘制时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "\n")

        landing_point_map = []  # 存储海缆登陆站字典列表
        with open(landing_point, 'r', encoding='utf-8') as landing_point_f:
            landing_point_dic = json.load(landing_point_f)
            for item in landing_point_dic["features"]:
                lp_dic = item["properties"]
                lp_dic["coordinates"] = item["geometry"]["coordinates"]
                landing_point_map.append(lp_dic)

        cable_line_map = []  # 存储海缆路由字典列表
        cable_line_map_all = []  # 许多海缆成鱼骨状，需要形成多条记录
        with open(cable_line, 'r', encoding='utf-8') as cable_line_f:
            cable_line_dic = json.load(cable_line_f)
            for item in cable_line_dic["features"]:
                cl_dic = item["properties"]
                cl_dic["color"] = hex_to_rgb(cl_dic["color"])
                cable_line_map.append(cl_dic)
                for multi_path in item["geometry"]["coordinates"]:
                    cl_dic_temp = cl_dic.copy()  # 创建新独立字典
                    # print("multi_path", multi_path)
                    cl_dic_temp["path"] = multi_path
                    if is_single_cable_mode:
                        if cl_dic_temp["name"] == single_cable_name:
                            cable_line_map_all.append(cl_dic_temp)
                    else:
                        if cl_dic_temp["name"] in cable_name_list:
                            cable_line_map_all.append(cl_dic_temp)

                    del cl_dic_temp  # 销毁该字典

        layer_scatter_lp = pdk.Layer(
            "ScatterplotLayer",
            landing_point_map,
            pickable=True,  # 可选择
            opacity=0.8,  # 透明度
            stroked=True,  # 绘制点的轮廓
            filled=True,  # 绘制点的填充区
            radius_scale=6,  # 所有点的全局半径乘数
            radius_min_pixels=map_point_radius,  # 点半径的最小值
            radius_max_pixels=100,  # 点半径的最大值
            line_width_min_pixels=1,  # 线的最小的像素值
            get_position="coordinates",  # 获取位置信息
            # get_fill_color=[255, 140, 0],  # 填充的颜色
            get_fill_color=hex_to_rgb(map_point_color),
            get_line_color=[0, 0, 0])

        layer_heatmap_lp = pdk.Layer(
            "HeatmapLayer",
            landing_point_map if is_heatmap_mode else [],
            opacity=0.9,
            get_position="coordinates")

        layer_hexagon_lp = pdk.Layer(
            'HexagonLayer',  # `type` positional argument is here, CPUGridLayer, HexagonLayer,GridLayer
            landing_point_map if is_hexagon_mode else [],
            get_position="coordinates",
            auto_highlight=True,
            elevation_scale=100,
            pickable=True,
            elevation_range=[10, 3000],
            extruded=True,
            coverage=1,
            radius=10, )

        layer_path_cable = pdk.Layer(
            type="PathLayer",
            data=cable_line_map_all,
            pickable=True,
            get_color="color",
            width_scale=20,
            width_min_pixels=map_line_width,
            get_path="path",
            get_width=5,
        )

        # Set the viewport location
        view_state = pdk.ViewState(
            longitude=0,
            latitude=0,
            zoom=2,
            min_zoom=2,
            max_zoom=22,
            pitch=45,
            bearing=0)
        # Combined all of it and render a viewport
        r = pdk.Deck(map_style=map_style,
                     layers=[layer_hexagon_lp, layer_heatmap_lp, layer_path_cable, layer_scatter_lp],
                     initial_view_state=view_state,
                     tooltip={
                         # 'html': '<b>Elevation Value:</b> {elevationValue}',
                         'text': '{name}',
                         'style': {
                             'color': 'white'
                         },
                     }
                     )
        st.pydeck_chart(r)
        st.write("海缆数量总计：", len(cable_list_country))
        st.write("其中已投入使用的数量：", len(is_used_list))
        with st.expander("详细列表", False):
            st.json(is_used_list)
        st.write("正在建设中的数量:", len(is_planed_list))
        with st.expander("详细列表", False):
            st.json(is_planed_list)
    elif choice == "俄罗斯":
        country_cable_file = "./map_physical/cable_v3/country/russia.json"
        cable_list_country = []  # 存储该国所有海缆
        with open(country_cable_file, 'r', encoding='utf-8') as f:
            country_cable_dic = json.load(f)
            for item in country_cable_dic["cables"]:
                cable_list_country.append(item)
        is_planed_list = [item for item in cable_list_country if item["is_planned"]]
        is_used_list = [item for item in cable_list_country if not item["is_planned"]]
        cable_name_list = [item["name"] for item in cable_list_country]
        single_cable_name = st.selectbox("请选择或搜索需要了解的海缆（需开启Single模式）:", cable_name_list)

        st.write("深度整合开源GIS地图系统，构建全球各国物理层地图绘制（Submarine Cables Map）— ", choice)
        st.write("地图绘制时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "\n")

        landing_point_map = []  # 存储海缆登陆站字典列表
        with open(landing_point, 'r', encoding='utf-8') as landing_point_f:
            landing_point_dic = json.load(landing_point_f)
            for item in landing_point_dic["features"]:
                lp_dic = item["properties"]
                lp_dic["coordinates"] = item["geometry"]["coordinates"]
                landing_point_map.append(lp_dic)

        cable_line_map = []  # 存储海缆路由字典列表
        cable_line_map_all = []  # 许多海缆成鱼骨状，需要形成多条记录
        with open(cable_line, 'r', encoding='utf-8') as cable_line_f:
            cable_line_dic = json.load(cable_line_f)
            for item in cable_line_dic["features"]:
                cl_dic = item["properties"]
                cl_dic["color"] = hex_to_rgb(cl_dic["color"])
                cable_line_map.append(cl_dic)
                for multi_path in item["geometry"]["coordinates"]:
                    cl_dic_temp = cl_dic.copy()  # 创建新独立字典
                    # print("multi_path", multi_path)
                    cl_dic_temp["path"] = multi_path
                    if is_single_cable_mode:
                        if cl_dic_temp["name"] == single_cable_name:
                            cable_line_map_all.append(cl_dic_temp)
                    else:
                        if cl_dic_temp["name"] in cable_name_list:
                            cable_line_map_all.append(cl_dic_temp)

                    del cl_dic_temp  # 销毁该字典

        layer_scatter_lp = pdk.Layer(
            "ScatterplotLayer",
            landing_point_map,
            pickable=True,  # 可选择
            opacity=0.8,  # 透明度
            stroked=True,  # 绘制点的轮廓
            filled=True,  # 绘制点的填充区
            radius_scale=6,  # 所有点的全局半径乘数
            radius_min_pixels=map_point_radius,  # 点半径的最小值
            radius_max_pixels=100,  # 点半径的最大值
            line_width_min_pixels=1,  # 线的最小的像素值
            get_position="coordinates",  # 获取位置信息
            # get_fill_color=[255, 140, 0],  # 填充的颜色
            get_fill_color=hex_to_rgb(map_point_color),
            get_line_color=[0, 0, 0])

        layer_heatmap_lp = pdk.Layer(
            "HeatmapLayer",
            landing_point_map if is_heatmap_mode else [],
            opacity=0.9,
            get_position="coordinates")

        layer_hexagon_lp = pdk.Layer(
            'HexagonLayer',  # `type` positional argument is here, CPUGridLayer, HexagonLayer,GridLayer
            landing_point_map if is_hexagon_mode else [],
            get_position="coordinates",
            auto_highlight=True,
            elevation_scale=100,
            pickable=True,
            elevation_range=[10, 3000],
            extruded=True,
            coverage=1,
            radius=10, )

        layer_path_cable = pdk.Layer(
            type="PathLayer",
            data=cable_line_map_all,
            pickable=True,
            get_color="color",
            width_scale=20,
            width_min_pixels=map_line_width,
            get_path="path",
            get_width=5,
        )

        # Set the viewport location
        view_state = pdk.ViewState(
            longitude=0,
            latitude=0,
            zoom=2,
            min_zoom=2,
            max_zoom=22,
            pitch=45,
            bearing=0)
        # Combined all of it and render a viewport
        r = pdk.Deck(map_style=map_style,
                     layers=[layer_hexagon_lp, layer_heatmap_lp, layer_path_cable, layer_scatter_lp],
                     initial_view_state=view_state,
                     tooltip={
                         # 'html': '<b>Elevation Value:</b> {elevationValue}',
                         'text': '{name}',
                         'style': {
                             'color': 'white'
                         },
                     }
                     )
        st.pydeck_chart(r)
        st.write("海缆数量总计：", len(cable_list_country))
        st.write("其中已投入使用的数量：", len(is_used_list))
        with st.expander("详细列表", False):
            st.json(is_used_list)
        st.write("正在建设中的数量:", len(is_planed_list))
        with st.expander("详细列表", False):
            st.json(is_planed_list)
    elif choice == "日本":
        country_cable_file = "./map_physical/cable_v3/country/japan.json"
        cable_list_country = []  # 存储该国所有海缆
        with open(country_cable_file, 'r', encoding='utf-8') as f:
            country_cable_dic = json.load(f)
            for item in country_cable_dic["cables"]:
                cable_list_country.append(item)
        is_planed_list = [item for item in cable_list_country if item["is_planned"]]
        is_used_list = [item for item in cable_list_country if not item["is_planned"]]
        cable_name_list = [item["name"] for item in cable_list_country]
        single_cable_name = st.selectbox("请选择或搜索需要了解的海缆（需开启Single模式）:", cable_name_list)

        st.write("深度整合开源GIS地图系统，构建全球各国物理层地图绘制（Submarine Cables Map）— ", choice)
        st.write("地图绘制时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "\n")

        landing_point_map = []  # 存储海缆登陆站字典列表
        with open(landing_point, 'r', encoding='utf-8') as landing_point_f:
            landing_point_dic = json.load(landing_point_f)
            for item in landing_point_dic["features"]:
                lp_dic = item["properties"]
                lp_dic["coordinates"] = item["geometry"]["coordinates"]
                landing_point_map.append(lp_dic)

        cable_line_map = []  # 存储海缆路由字典列表
        cable_line_map_all = []  # 许多海缆成鱼骨状，需要形成多条记录
        with open(cable_line, 'r', encoding='utf-8') as cable_line_f:
            cable_line_dic = json.load(cable_line_f)
            for item in cable_line_dic["features"]:
                cl_dic = item["properties"]
                cl_dic["color"] = hex_to_rgb(cl_dic["color"])
                cable_line_map.append(cl_dic)
                for multi_path in item["geometry"]["coordinates"]:
                    cl_dic_temp = cl_dic.copy()  # 创建新独立字典
                    # print("multi_path", multi_path)
                    cl_dic_temp["path"] = multi_path
                    if is_single_cable_mode:
                        if cl_dic_temp["name"] == single_cable_name:
                            cable_line_map_all.append(cl_dic_temp)
                    else:
                        if cl_dic_temp["name"] in cable_name_list:
                            cable_line_map_all.append(cl_dic_temp)

                    del cl_dic_temp  # 销毁该字典

        layer_scatter_lp = pdk.Layer(
            "ScatterplotLayer",
            landing_point_map,
            pickable=True,  # 可选择
            opacity=0.8,  # 透明度
            stroked=True,  # 绘制点的轮廓
            filled=True,  # 绘制点的填充区
            radius_scale=6,  # 所有点的全局半径乘数
            radius_min_pixels=map_point_radius,  # 点半径的最小值
            radius_max_pixels=100,  # 点半径的最大值
            line_width_min_pixels=1,  # 线的最小的像素值
            get_position="coordinates",  # 获取位置信息
            # get_fill_color=[255, 140, 0],  # 填充的颜色
            get_fill_color=hex_to_rgb(map_point_color),
            get_line_color=[0, 0, 0])

        layer_heatmap_lp = pdk.Layer(
            "HeatmapLayer",
            landing_point_map if is_heatmap_mode else [],
            opacity=0.9,
            get_position="coordinates")

        layer_hexagon_lp = pdk.Layer(
            'HexagonLayer',  # `type` positional argument is here, CPUGridLayer, HexagonLayer,GridLayer
            landing_point_map if is_hexagon_mode else [],
            get_position="coordinates",
            auto_highlight=True,
            elevation_scale=100,
            pickable=True,
            elevation_range=[10, 3000],
            extruded=True,
            coverage=1,
            radius=10, )

        layer_path_cable = pdk.Layer(
            type="PathLayer",
            data=cable_line_map_all,
            pickable=True,
            get_color="color",
            width_scale=20,
            width_min_pixels=map_line_width,
            get_path="path",
            get_width=5,
        )

        # Set the viewport location
        view_state = pdk.ViewState(
            longitude=0,
            latitude=0,
            zoom=2,
            min_zoom=2,
            max_zoom=22,
            pitch=45,
            bearing=0)
        # Combined all of it and render a viewport
        r = pdk.Deck(map_style=map_style,
                     layers=[layer_hexagon_lp, layer_heatmap_lp, layer_path_cable, layer_scatter_lp],
                     initial_view_state=view_state,
                     tooltip={
                         # 'html': '<b>Elevation Value:</b> {elevationValue}',
                         'text': '{name}',
                         'style': {
                             'color': 'white'
                         },
                     }
                     )
        st.pydeck_chart(r)
        st.write("海缆数量总计：", len(cable_list_country))
        st.write("其中已投入使用的数量：", len(is_used_list))
        with st.expander("详细列表", False):
            st.json(is_used_list)
        st.write("正在建设中的数量:", len(is_planed_list))
        with st.expander("详细列表", False):
            st.json(is_planed_list)
    elif choice == "中国台湾":
        country_cable_file = "./map_physical/cable_v3/country/taiwan.json"
        cable_list_country = []  # 存储该国所有海缆
        with open(country_cable_file, 'r', encoding='utf-8') as f:
            country_cable_dic = json.load(f)
            for item in country_cable_dic["cables"]:
                cable_list_country.append(item)
        is_planed_list = [item for item in cable_list_country if item["is_planned"]]
        is_used_list = [item for item in cable_list_country if not item["is_planned"]]
        cable_name_list = [item["name"] for item in cable_list_country]
        single_cable_name = st.selectbox("请选择或搜索需要了解的海缆（需开启Single模式）:", cable_name_list)

        st.write("深度整合开源GIS地图系统，构建全球各国物理层地图绘制（Submarine Cables Map）— ", choice)
        st.write("地图绘制时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "\n")

        landing_point_map = []  # 存储海缆登陆站字典列表
        with open(landing_point, 'r', encoding='utf-8') as landing_point_f:
            landing_point_dic = json.load(landing_point_f)
            for item in landing_point_dic["features"]:
                lp_dic = item["properties"]
                lp_dic["coordinates"] = item["geometry"]["coordinates"]
                landing_point_map.append(lp_dic)

        cable_line_map = []  # 存储海缆路由字典列表
        cable_line_map_all = []  # 许多海缆成鱼骨状，需要形成多条记录
        with open(cable_line, 'r', encoding='utf-8') as cable_line_f:
            cable_line_dic = json.load(cable_line_f)
            for item in cable_line_dic["features"]:
                cl_dic = item["properties"]
                cl_dic["color"] = hex_to_rgb(cl_dic["color"])
                cable_line_map.append(cl_dic)
                for multi_path in item["geometry"]["coordinates"]:
                    cl_dic_temp = cl_dic.copy()  # 创建新独立字典
                    # print("multi_path", multi_path)
                    cl_dic_temp["path"] = multi_path
                    if is_single_cable_mode:
                        if cl_dic_temp["name"] == single_cable_name:
                            cable_line_map_all.append(cl_dic_temp)
                    else:
                        if cl_dic_temp["name"] in cable_name_list:
                            cable_line_map_all.append(cl_dic_temp)

                    del cl_dic_temp  # 销毁该字典

        layer_scatter_lp = pdk.Layer(
            "ScatterplotLayer",
            landing_point_map,
            pickable=True,  # 可选择
            opacity=0.8,  # 透明度
            stroked=True,  # 绘制点的轮廓
            filled=True,  # 绘制点的填充区
            radius_scale=6,  # 所有点的全局半径乘数
            radius_min_pixels=map_point_radius,  # 点半径的最小值
            radius_max_pixels=100,  # 点半径的最大值
            line_width_min_pixels=1,  # 线的最小的像素值
            get_position="coordinates",  # 获取位置信息
            # get_fill_color=[255, 140, 0],  # 填充的颜色
            get_fill_color=hex_to_rgb(map_point_color),
            get_line_color=[0, 0, 0])

        layer_heatmap_lp = pdk.Layer(
            "HeatmapLayer",
            landing_point_map if is_heatmap_mode else [],
            opacity=0.9,
            get_position="coordinates")

        layer_hexagon_lp = pdk.Layer(
            'HexagonLayer',  # `type` positional argument is here, CPUGridLayer, HexagonLayer,GridLayer
            landing_point_map if is_hexagon_mode else [],
            get_position="coordinates",
            auto_highlight=True,
            elevation_scale=100,
            pickable=True,
            elevation_range=[10, 3000],
            extruded=True,
            coverage=1,
            radius=10, )

        layer_path_cable = pdk.Layer(
            type="PathLayer",
            data=cable_line_map_all,
            pickable=True,
            get_color="color",
            width_scale=20,
            width_min_pixels=map_line_width,
            get_path="path",
            get_width=5,
        )

        # Set the viewport location
        view_state = pdk.ViewState(
            longitude=0,
            latitude=0,
            zoom=2,
            min_zoom=2,
            max_zoom=22,
            pitch=45,
            bearing=0)
        # Combined all of it and render a viewport
        r = pdk.Deck(map_style=map_style,
                     layers=[layer_hexagon_lp, layer_heatmap_lp, layer_path_cable, layer_scatter_lp],
                     initial_view_state=view_state,
                     tooltip={
                         # 'html': '<b>Elevation Value:</b> {elevationValue}',
                         'text': '{name}',
                         'style': {
                             'color': 'white'
                         },
                     }
                     )
        st.pydeck_chart(r)
        st.write("海缆数量总计：", len(cable_list_country))
        st.write("其中已投入使用的数量：", len(is_used_list))
        with st.expander("详细列表", False):
            st.json(is_used_list)
        st.write("正在建设中的数量:", len(is_planed_list))
        with st.expander("详细列表", False):
            st.json(is_planed_list)


else:
    st.info("请先点击首页下拉选择框，登录系统！")
