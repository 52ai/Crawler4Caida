# coding:utf-8
"""
create on Jan 2,2020 By Wayne YU
Function:
尝试使用Folium绘制地理地图

"""

import folium
import pandas as pd

cdata = pd.read_csv('https://cocl.us/sanfran_crime_dataset')
print(cdata.head())
# m = folium.Map(location=[30.5441635964541, 114.153920782153], zoom_start=13, tiles="Stamen Terrain")

m = folium.Map(location=[39.9213364, 116.3527165], zoom_start=12)

tooltip = 'Click me!'

folium.Marker([30.5441635964541, 114.153920782153], popup='<i>AS4134</i>', tooltip=tooltip).add_to(m)
folium.Marker([39.8959270178956, 116.418913155767], popup='<b>AS4847</b>', tooltip=tooltip).add_to(m)

m.save('D:/Code/Crawler4Caida/021Folium/index.html')

