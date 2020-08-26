# coding:utf-8
"""
create on Aug 26, 2020 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:


本程序主要是为了梳理Telegeography的全球海缆数据，根据其Github库，其原数据分为四个文件夹

一、cable文件夹，为全部的海缆json文件，一个json文件代表一根海缆，共计472条。包含如下字段：
id: 2africa
name: 2Africa
cable_id: 2020
landing_points:[{},]
length: 37,000 km
rfs: 2023
owners: Facebook,  Vodafone,  MTN Group,  China Mobile,  WIOCC,  Orange,  Telecom Egypt,  Saudi Telecom
url: https://www.2africacable.com/
notes：null

二、country文件夹，为全部的国家json文件，一个json文件代表一个国家登陆海缆信息，共计180个国家。包含如下字段：

name: China
cables:[{},]
landing_points: [{},]
latlon: [{},]

三、landing-point文件夹，为全部海缆登陆点json文件，一个json文件代表一个海缆登陆点信息，共计1242个海缆登陆点。包括如下字段：

city_id: 5082
id: chongming-china
latitude: 31.619880
longtitude: 121.395212
name: Chongming, China
type: landing_point
cables: [{}, ]

四、ready-for-service文件夹，为当年开通海缆和登陆点信息，共有1989年-2023年，35年的数据。包括如下字段：

rfs: 2020
cables: [{}, ]
landing_points: [{}, ]


以上是Telegeography全部的全球海缆源数据，我需要认真思考，基于这份数据，我能够做一些什么样的分析

先从极图的绘制数据开始吧

以海缆登陆城市为点，以城市间的海缆连接为线，绘制极图
城市，国家，经纬度，海缆（导出海缆数量，每条海缆开通年份，每条海缆的长度，城市级的海缆互联关系）

其实根本不同转换json文件，直接读取json文件，根据格式获取相应的数据即可
json文件本质上就是Python里面的字典

"""
import json
import time


def read_single_json(json_file):
    """
    根据传入的json文件，将其读取json对象
    :param json_file:
    :return:
    """
    with open(json_file, 'r') as load_f:
        load_dict = json.load(load_f)
        print(load_dict)

    return load_dict


if __name__ == "__main__":
    time_start = time.time()  # 记录程序启动的时间
    my_json_file = "../000LocalData/CableMap/v2/cable/2africa.json"
    read_single_json(my_json_file)
    time_end = time.time()  # 记录程序结束的时间
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")


