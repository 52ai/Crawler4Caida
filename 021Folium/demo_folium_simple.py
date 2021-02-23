# coding:utf-8
"""
create on Feb 8, 2020 By Wayne YU

Function:

进一步研究Folium的各种功能

"""
import folium
from folium import plugins

latitude = 39.9213364
longitude = 116.3527165

m = folium.Map(location=[latitude, longitude], zoom_start=4)
tooltip = 'Click me!'
folium.Marker([30.54, 114.15], popup='<i>AS4134</i>', tooltip=tooltip).add_to(m)
folium.Marker([39.89, 116.41], popup='<b>AS4847</b>', tooltip=tooltip).add_to(m)
folium.Marker([35.61, 139.05], popup='<b>AS173</b>', tooltip=tooltip).add_to(m)

plugins.PolyLineOffset([[30.54, 114.15], [39.89, 116.41]], color='green').add_to(m)
plugins.PolyLineOffset([[39.89, 116.41], [35.61, 139.05]], color='red').add_to(m)

m.save("as_geo_map.html")
