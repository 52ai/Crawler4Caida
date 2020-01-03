# coding:utf-8
"""
create on Jan 2,2020 By Wayne YU
Function:
尝试使用Folium绘制地理地图

"""

import folium


m = folium.Map(location=[39, 116], zoom_start=13)

tooltip = 'Click me!'

folium.Marker([39.3288, 116.6625], popup='<i>Mt. Hood Meadows</i>', tooltip=tooltip).add_to(m)
folium.Marker([39.3288, 116.1125], popup='<b>Timberline Lodge</b>', tooltip=tooltip).add_to(m)

m.save('index.html')

