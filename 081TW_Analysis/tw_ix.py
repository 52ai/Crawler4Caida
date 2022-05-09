# coding:utf-8
"""
create on May 9, 2022 By Wayne YU
Email:ieeflsyu@outlook.com

Function:
分析TW地区交换中心情况，包括地理位置、接入网络、接入带宽、成立时间等

PeeringDB的IX信息（https://www.peeringdb.com/api/ix）
{'id': 1,
'org_id': 2,
'name': 'Equinix Ashburn',
'name_long': 'Equinix Ashburn Exchange',
'city': 'Ashburn',
'country': 'US',
'region_continent': 'North America',
'media': 'Ethernet',
'notes': '',
'proto_unicast': True,
'proto_multicast': False,
'proto_ipv6': True,
'website': 'https://ix.equinix.com',
'url_stats': '',
'tech_email': 'support@equinix.com',
'tech_phone': '',
'policy_email': 'support@equinix.com',
'policy_phone': '',
'net_count': 324,
'created': '2010-07-29T00:00:00Z',
'updated': '2016-11-23T21:40:34Z',
'status': 'ok'}

ix的详细信息：
{"id": 26,
"org_id": 2634,
"org": {"id": 2634,
        "name": "Amsterdam Internet Exchange BV",
        "aka": "",
        "name_long": "",
        "website": "http://www.ams-ix.net/",
        "notes": "",
        "net_set": [3363, 4277, 6471, 14259, 14260],
        "fac_set": [],
        "ix_set": [26, 366, 577, 935, 944, 1623],
        "address1": "Frederiksplein 42",
        "address2": "",
        "city": "Amsterdam",
        "country": "NL",
        "state": "Noord Holland",
        "zipcode": "1017XN",
        "floor": "",
        "suite": "",
        "latitude": null,
        "longitude": null,
        "created": "2010-08-11T15:40:42Z",
        "updated": "2020-02-19T04:08:04Z",
        "status": "ok"},
"name": "AMS-IX",
"aka": "",
"name_long": "Amsterdam Internet Exchange",
"city": "Amsterdam",
"country": "NL",
"region_continent": "Europe",
"media": "Ethernet",
"notes": "",
"proto_unicast": true,
"proto_multicast": false,
"proto_ipv6": true,
"website": "http://www.ams-ix.net/",
"url_stats": "https://www.ams-ix.net/statistics/",
"tech_email": "noc@ams-ix.net",
"tech_phone": "+31205141717",
"policy_email": "info@ams-ix.net",
"policy_phone": "+31203058999",
"fac_set": [...],
"ixlan_set": [...],
"net_count": 820,
"fac_count": 25,
"ixf_net_count": 0,
"ixf_last_import": null,
"service_level": "Not Disclosed",
"terms": "Not Disclosed",
"created": "2010-07-29T00:00:00Z",
"updated": "2020-01-22T04:24:06Z",
"status": "ok"}]

思路：
根据国别筛选出，IX记录，包含ID、简称、全称、城市、国家、大洲、官网、联系方式、接入网络数量、创建时间、更新时间

"""

from urllib.request import urlopen
import json
from datetime import *
import time


def gain_as2country_caida():
    """
    根据Caida asn info获取as对应的国家信息
    :return as2country:
    """
    as_info_file = '..\\000LocalData\\as_Gao\\asn_info_from_caida.csv'
    as2country = {}  # 存储as号到country的映射关系
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split(",")
        # print(line)
        as_number = line[0]
        as_country = line[-1]
        as2country[as_number] = as_country
    return as2country


def gain_as2org_caida():
    """
    根据Caida asn info获取as对应的org信息
    :return as2country:
    """
    as_info_file = '..\\000LocalData\\as_Gao\\asn_info_from_caida.csv'
    as2org_dic = {}  # 存储as号到country的映射关系
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split(",")
        # print(line)
        as_number = line[0]
        as_org = line[2] + "," + line[1]
        as2org_dic[as_number] = as_org
    return as2org_dic


def ix_analysis(aim_country):
    """
    根据PEERING DB数据，生成目标国家的交换中心设施情况
    :param aim_country:
    :return:
    """
    as2country = gain_as2country_caida()
    as2org = gain_as2org_caida()
    print(f"- - - - - - - {aim_country}国家网络地图统计报告（交换中心）- - - - - -  - - ")
    print("0.报告生成时间：", datetime.now())
    # html = urlopen(r"https://www.peeringdb.com/api/ix")
    # html_json = json.loads(html.read())
    with open("../000LocalData/IXVis/ix20220509.json") as json_file:
        html_json = json.load(json_file)

    ix_aim = []  # 统计目标国家和地区的IX情况

    for item in html_json['data']:

        temp = []
        if item['country'] == aim_country:
            temp.append(item['id'])
            temp.append(item['name'])
            temp.append(item['name_long'])
            temp.append(item['city'])
            temp.append(item['country'])
            temp.append(item['region_continent'])
            temp.append(item['website'])
            temp.append(item['tech_email'])
            temp.append(item['net_count'])
            temp.append(item['created'])
            temp.append(item['updated'])
            ix_aim.append(temp)

    ix_aim.sort(reverse=True, key=lambda elem: int(elem[-3]))
    print("1.全球IXP总数:", len(html_json['data']))
    print(f"2.{aim_country}共有{len(ix_aim)}个互联网交换中心，详情如下（按照接入网络数量排名）:")
    for item in ix_aim:
        print([item[1], item[2], item[3], item[6], item[8], item[9]])
    """
    根据目标国家的交换中心ID，进一步研究TOP IX的详细信息
    如接入网络详情、接入带宽详情
    统计数据源:https://www.peeringdb.com/api/netixlan
    
    {"id": 589, 
    "net_id": 120, 
    "ix_id": 1, 
    "name": "Equinix Ashburn", 
    "ixlan_id": 1, 
    "notes": "", 
    "speed": 10000, 
    "asn": 12322, 
    "ipaddr4": "206.126.236.160", 
    "ipaddr6": "2001:504:0:2:0:1:2322:1", 
    "is_rs_peer": false, 
    "operational": true, 
    "created": "2010-07-29T00:00:00Z", 
    "updated": "2020-03-06T19:27:03Z", 
    "status": "ok"}, 
    """
    # html = urlopen(r"https://www.peeringdb.com/api/netixlan")
    # html_json = json.loads(html.read())
    with open("../000LocalData/IXVis/netixlan20220509.json") as json_file:
        html_json = json.load(json_file)
    net_ix_result = []  # 存储网络接入IX的数据
    except_as_list = []  # 存储异常的AS列表
    print("- - - - - - - - - - - - - - - - - - ")
    print("根据目标国家的交换中心ID，进一步研究TOP IX的详细信息")
    for ix_item in ix_aim[0:2]:
        print("- - - - - - - - - - - - - - - - - - ")
        print("IX ID:", ix_item[0])
        print("IX NAME:", ix_item[2])
        print("接入网络数量:", ix_item[8])
        aim_ix_result = []  # 存储目标ix接入网络基本信息
        for item in html_json['data']:
            if item['ix_id'] == ix_item[0]:
                temp_list = []  # 存储目标IX接入网络的情况
                as_country = "ZZ"
                as_org = "ZZ"
                try:
                    as_country = as2country[str(item['asn'])]
                except Exception as e:
                    except_as_list.append(e)

                try:
                    as_org = as2org[str(item['asn'])]
                except Exception as e:
                    except_as_list.append(e)
                temp_list.append("AS"+str(item['asn']))
                temp_list.append(as_org)
                temp_list.append(as_country)
                temp_list.append(item['speed'])
                # print(temp_list)
                aim_ix_result.append(temp_list)
        aim_ix_result.sort(reverse=True, key=lambda elem: int(elem[-1]))
        total_speed = 0
        for item in aim_ix_result:
            print(item)
            total_speed += item[-1]
        print("合计接入带宽:", total_speed)

        print("其中涉及CN网络为:")
        total_speed_cn = 0
        for item in aim_ix_result:
            if item[2] == "CN":
                print(item)
                total_speed_cn += item[-1]
        print("合计接入带宽（CN）:", total_speed_cn)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    country = "TW"
    ix_analysis(country)
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")

