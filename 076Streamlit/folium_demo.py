import streamlit as st
import folium
from streamlit_folium import folium_static
st.set_page_config(page_title="网页地图应用", layout="centered")
my_map= folium.Map(location=[31.23374, 121.46819],zoom_start=20, tiles="Stamen Terrain")
basemaps = {
    'Google Maps': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Maps',
        overlay = True,
        control = True
    ),
    'Google Satellite': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Satellite',
        overlay = True,
        control = True
    ),
    'Google Terrain': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Terrain',
        overlay = True,
        control = True
    ),
    'Google Satellite Hybrid': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Satellite',
        overlay = True,
        control = True
    ),
    'Esri Satellite': folium.TileLayer(
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr = 'Esri',
        name = 'Esri Satellite',
        overlay = True,
        control = True
    ),
    '腾讯地图': folium.TileLayer(
        tiles = 'http://rt0.map.gtimg.com/realtimerender?z={z}&x={x}&y={-y}&type=vector&style=0',
        attr = '腾讯地图',
        name = '腾讯地图',
        overlay = True,
        control = True
    ),
    '高德卫星地图': folium.TileLayer(
        tiles = 'https://webst01.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}',
        attr = '高德卫星地图',
        name = '高德卫星地图',
        overlay = True,
        control = True
    )

}

map_select=st.selectbox("请选择一个要查看的地图类型",("Google Maps", "Esri Satellite","高德卫星地图","腾讯地图"))
basemaps[map_select].add_to(my_map)

folium.Marker([45.3288, -121.6625], popup="<i>Mt. Hood Meadows</i>").add_to(my_map)

folium_static(my_map)


st.info("地图标记")
lon = st.text_input("请输入要标记点的经度", value="121.46819")
lat = st.text_input("请输入要标记点的纬度", value="31.23374")

m = folium.Map(location=[lat, lon], zoom_start=20, tiles="Stamen Terrain")

tooltip = "我在这里!"
folium.Marker([lat, lon], popup="<i>Mt. Hood Meadows</i>", tooltip=tooltip, icon=folium.Icon(color="red",icon="cloud")).add_to(m)

folium_static(m)