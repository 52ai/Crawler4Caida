# coding:utf-8
from urllib.request import urlopen
import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import *

html = urlopen(r'https://www.peeringdb.com/api/ix')
hjson = json.loads(html.read())
# print "IX Count:", len(hjson['data']),"(2016年整个互联网有465个IXP)"
# print hjson['data'][0]
print("IX Count:", len(hjson['data']),"(2016年整个互联网有465个IXP)")
print(hjson['data'][0])

dic_country = {}
dic_region = {}
dic_city_us = {}
ixp_cn = []  # 中国大陆的IXP
ixp_hk = []  # 香港地区
ixp_tw = []  # 台湾地区
ixp_cnt_year = {}  # 统计每年ixp的数量

for item in hjson['data']:
    # print item['name'], item['city'], item['country'], item['region_continent']
    if item['country'] not in dic_country:
        dic_country[item['country']] = 1
    else:
        dic_country[item['country']] = dic_country[item['country']] + 1

    if item['region_continent'] not in dic_region:
        dic_region[item['region_continent']] = 1
    else:
        dic_region[item['region_continent']] = dic_region[item['region_continent']] + 1

    if item['country'] == 'US':
        if item['city'] not in dic_city_us:
            dic_city_us[item['city']] = 1
        else:
            dic_city_us[item['city']] = dic_city_us[item['city']] + 1
    temp = []
    if item['country'] == 'CN':
        temp.append(item['name'])
        temp.append(item['created'])
        temp.append(item['website'])
        temp.append(item['name_long'])
        ixp_cn.append(temp)

    temp = []
    if item['country'] == 'HK':
        temp.append(item['name'])
        temp.append(item['created'])
        temp.append(item['website'])
        temp.append(item['name_long'])
        ixp_hk.append(temp)

    temp = []
    if item['country'] == 'TW':
        temp.append(item['name'])
        temp.append(item['created'])
        temp.append(item['website'])
        temp.append(item['name_long'])
        ixp_tw.append(temp)

    # 利用datetime处理时间
    dt = datetime.strptime(item['created'], '%Y-%m-%dT%H:%M:%SZ')
    # print dt.year

    # 从世界的角度的来看每年的新增ixp
    if dt.year not in ixp_cnt_year:
        ixp_cnt_year[int(dt.year)] = 1
    else:
        ixp_cnt_year[int(dt.year)] = ixp_cnt_year[int(dt.year)] + 1


print("整个互联网从2010年至今，每年的新增的ixp数量")
for item in ixp_cnt_year:
    print(item, ":", ixp_cnt_year[item])


print("统计整个互联网从2010年至今，每年总的ixp数量")
cnt_list = [0, 0, 0, 0, 0, 0, 0, 0]
for year in ixp_cnt_year.keys():
    for i in range((year-2010),8):
        cnt_list[i] += ixp_cnt_year[year]

print(cnt_list)

# y = cnt_list
# x = range(2010,2018)
#
# plt.plot(x, y, marker='+', mec='r', mfc='w')
# plt.title('The entire Internet IXP number per year')
# plt.xlabel('Year')
# plt.ylabel('IXP Number')
# plt.show()


Y1 = []
country_name = []
print("用有IXP数量较多的几个国家：")
for item in dic_country.keys():
    if dic_country[item] >= 20:
        country_name.append(item)
        Y1.append(dic_country[item])
        print(item, ":", dic_country[item])

print("CN:", len(ixp_cn))

# print("截止2017年10月29日，国内IXP由2016年的6个增加到10个，其信息如下：")
print("截止2019年10月25日，国内IXP由2016年的6个增加到13个，其信息如下：")
for item in ixp_cn:
    print(item[0], ",", item[1], ",", item[2], ",", item[3])
    # print item[0], ",", item[1]

print("香港地区HK的IXP数量:", len(ixp_hk), "其详细信息如下：")
for item in ixp_hk:
    print(item[0], ",", item[1], ",", item[2], ",", item[3])


print("台湾地区TW的IXP数量:", len(ixp_tw), "其详细信息如下：")
for item in ixp_tw:
    print(item[0], ",", item[1], ",", item[2], ",", item[3])


# country_name.append('CN')
# Y1.append(len(ixp_cn))
# X1 = np.arange(len(Y1))
# plt.bar(X1, Y1)
# plt.xticks(X1, country_name)
# plt.title('The distribution of IXP on some countries')
# plt.xlabel('Country')
# plt.ylabel('Number')
# plt.show()

print("值得关注的是美国IXP数量由2016年的86个，增加到目前的117个，俄罗斯则从21个增加到36个")
Y2 = []
region_name = []
print("各大洲IXP的分布情况")
for item in dic_region.keys():
    region_name.append(item)
    Y2.append(dic_region[item])
    print(item, ":", dic_region[item])

# X2 = np.arange(len(Y2))
# plt.bar(X2, Y2)
# plt.xticks(X2, region_name, fontsize=6)
# plt.title('The distribution of IXP on all continents')
# plt.xlabel('Region')
# plt.ylabel('Number')
# plt.show()

# print "美国各城市IXP的分布情况"
# for item in dic_city_us.keys():
#    print item, ":", dic_city_us[item]

