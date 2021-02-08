# coding:utf-8
"""
create on Jan 2,2020 By Wayne YU
Function:
尝试使用Folium绘制地理地图

"""

import folium
import pandas as pd


# San Francisco latitude and longitude values
latitude = 37.77
longitude = -122.42

# Create map and display it
san_map = folium.Map(location=[latitude, longitude], zoom_start=12)


cdata = pd.read_csv('https://cocl.us/sanfran_crime_dataset')
print(cdata.head())

# get the first 200 crimes in the cdata
limit = 200
data = cdata.iloc[0:limit, :]

# Instantiate a feature group for the incidents in the dataframe
# incidents = folium.map.FeatureGroup()

# # Loop through the 200 crimes and add each to the incidents feature group
# for lat, lng, in zip(cdata.Y, data.X):
#     incidents.add_child(
#         folium.CircleMarker(
#             [lat, lng],
#             radius=7, # define how big you want the circle markers to be
#             color='yellow',
#             fill=True,
#             fill_color='red',
#             fill_opacity=0.4
#         )
#     )

# # Add incidents to map
# san_map = folium.Map(location=[latitude, longitude], zoom_start=12)
# san_map.add_child(incidents)


# # add pop-up text to each marker on the map
# latitudes = list(data.Y)
# longitudes = list(data.X)
# labels = list(data.Category)

# for lat, lng, label in zip(latitudes, longitudes, labels):
#     folium.Marker([lat, lng], popup=label).add_to(san_map)    
    
# # add incidents to map
# san_map.add_child(incidents)

from folium import plugins

# let's start again with a clean copy of the map of San Francisco
san_map = folium.Map(location=[latitude, longitude], zoom_start=12)

# instantiate a mark cluster object for the incidents in the dataframe
incidents = plugins.MarkerCluster().add_to(san_map)

# loop through the dataframe and add each data point to the mark cluster
for lat, lng, label, in zip(data.Y, data.X, cdata.Category):
    folium.Marker(
        location=[lat, lng],
        icon=None,
        popup=label,
    ).add_to(incidents)

# add incidents to map
san_map.add_child(incidents)


# from folium.plugins import HeatMap

# # let's start again with a clean copy of the map of San Francisco
# san_map = folium.Map(location = [latitude, longitude], zoom_start = 12)

# # Convert data format
# heatdata = data[['Y','X']].values.tolist()

# # add incidents to map
# HeatMap(heatdata).add_to(san_map)


# m = folium.Map(location=[30.5441635964541, 114.153920782153], zoom_start=13, tiles="Stamen Terrain")
# m = folium.Map(location=[39.9213364, 116.3527165], zoom_start=12)

# tooltip = 'Click me!'

# folium.Marker([30.5441635964541, 114.153920782153], popup='<i>AS4134</i>', tooltip=tooltip).add_to(m)
# folium.Marker([39.8959270178956, 116.418913155767], popup='<b>AS4847</b>', tooltip=tooltip).add_to(m)

# m.save('D:/Code/Crawler4Caida/021Folium/index.html')

san_map.save('D:/Code/Crawler4Caida/021Folium/index.html')
