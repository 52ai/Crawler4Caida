# coding:utf-8
"""
create on Jan 28, 2021 By Wenyan YU
Email: ieeflsyu@outloo.com

Function:

根据全球AS自治域网络关系，绘制地图

"""
import folium
from folium import plugins
from folium.plugins import HeatMap


# 读取Geo信息 
# ['399258', 'AS-JL-04 - Juul Labs  Inc.', 'US', '-118.958093', '37.2911673', 'SOURCE-G']
lati_list = []  # 存储维度
longi_list = []  # 存储经度
info_list = []  # 存储info 
asns_geo_all_file = 'D:/Code/Crawler4Caida/000LocalData/ASWhois/asns_geo_all.csv'
cnt = 1
with open(asns_geo_all_file, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.strip().split(",")
        if len(line) == 6 and cnt < 1000000 and line[2] == "CN":
            # print(line)
            lati = line[4]
            longi = line[3]
            as_info = "AS" + line[0] + "," + line[1] + "," + line[2] + "," + line[-1]
            lati_list.append(lati)
            longi_list.append(longi)
            info_list.append(as_info)
            cnt += 1

# location
latitude = 39.9213364
longitude = 116.3527165
print("LEN:", len(lati_list))
# Create map and display it
san_map = folium.Map(location=[latitude, longitude], zoom_start=5)
# instantiate a mark cluster object for the incidents in the dataframe
incidents = plugins.MarkerCluster().add_to(san_map)
# loop through the dataframe and add each data point to the mark cluster
for lat, lng, label in zip(lati_list, longi_list, info_list):
    folium.Marker(
        location=[lat, lng],
        icon=None,
        popup=label,
    ).add_to(incidents)

# add incidents to map
san_map.add_child(incidents)

# heatdata = zip(lati_list, longi_list)
# HeatMap(heatdata).add_to(san_map)

san_map.save('D:/Code/Crawler4Caida/058ASWhois/index.html')

