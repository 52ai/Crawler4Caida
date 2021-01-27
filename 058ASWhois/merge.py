# coding: utf-8
"""
create on Jan 26, 2021 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

对各种文件进行操作，最终实现多数据源的整合

asns_copy.csv + asyncio_log.csv = asns_geo_all.csv

"""
import csv


asns_geo_all_list = []  # 存储全部的AS Geo信息


# 读取asyncio_log.csv中机构的经纬度信息
asyncio_log_file =  'D:/Code/Crawler4Caida/000LocalData/ASWhois/asyncio_log.csv'
org_geo_dict = {}  # 存储机构的经纬度信息
with open(asyncio_log_file, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.strip().split(",")
        org_name = line[0].split(" - ")[0]
        logitude = line[1]
        latitude = line[2]
        # print(org_name, logitude, latitude)
        org_geo_dict[org_name] = [logitude, latitude]

# 读取asns_copy.csv 
ans_copy_file = 'D:/Code/Crawler4Caida/000LocalData/ASWhois/asns_copy.csv'
with open(ans_copy_file, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.strip().split(",")
        try:
            org_name = line[1].split(" - ")[-1]
        except Exception as e:
            print(e, line)
            continue
        temp_line = []
        if len(line) > 3:
            temp_line = line
            temp_line.append("SOURCE-C")
            asns_geo_all_list.append(temp_line)
        elif org_name in org_geo_dict.keys():
            temp_line = line
            temp_line.extend(org_geo_dict[org_name])
            temp_line.append("SOURCE-G")
            asns_geo_all_list.append(temp_line)
        else:
            temp_line = line
            temp_line.append("SOURCE-CHAWU")
            asns_geo_all_list.append(temp_line)

# 写文件
asns_geo_all_file = 'D:/Code/Crawler4Caida/000LocalData/ASWhois/asns_geo_all.csv'
with open(asns_geo_all_file, 'w', newline='', encoding='utf-8') as f:
    for item in asns_geo_all_list:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(item)

        
            




