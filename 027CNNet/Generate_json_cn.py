# coding:utf-8
"""
create on Feb 21, 2020 By Wayne YU
Function:

处理并生产相关json文件，用于生成Echarts

Version:2.0
Description：生成绘制json数据用于绘制中国AS网络互联星云图

"""

from urllib.request import urlopen
import json

# html = urlopen(r'http://static.popodv.com/data/attr/npmdep.json')
html = urlopen(r'http://static.popodv.com/data/attr/npmdep.json')
hjson = json.loads(html.read())
# print(hjson)
# print(hjson['nodes'])
# print(hjson['edges'])
# print(hjson['dependentsCount'])

nodes_list = []
edges_list = []
dependentsCount_list = []

# file_in = '..\\000LocalData\\as_cn\\as_map_caida_20200221.csv'
# bgp_file = "..\\000LocalData\\as_relationships\\serial-1\\20200201.as-rel.txt"

file_in = '..\\000LocalData\\as_cn\\as_map_gao_20200221.csv'
bgp_file = "..\\000LocalData\\as_Gao\\as_rel_gao_20200221_dict_up.txt"

file_read = open(file_in, 'r', encoding='utf-8')
map_asn2index = {}
asn_index = 0
cn_as_list = []
for line in file_read.readlines():
    line = line.strip().split('|')
    if line[6] == "CN":
        cn_as_list.append(line[0])
        nodes_str = line[5] + "(AS"+line[0]+")"
        nodes_list.append(nodes_str)
        dependentsCount_list.append(int(line[2]))
        map_asn2index[line[0]] = asn_index
        asn_index += 1

# print(nodes_list)
print("len(map_asn2index):", len(map_asn2index))
# print(map_asn2index)

"""
在上面的循环中，需要建立ASN与index Number的对应关系
"""
print("cn_as_list:", len(cn_as_list))
bgp_file_read = open(bgp_file, 'r', encoding='utf-8')
iter_cnt = 0
for line in bgp_file_read.readlines():
    if line.strip().find("#") == 0:
        continue
    line = line.strip().split('|')
    # print(line)
    if line[0] in cn_as_list and line[1] in cn_as_list:
        iter_cnt += 1
        try:
            source_index = map_asn2index[line[0]]
            destination_index = map_asn2index[line[1]]
            # print(source_index, destination_index)
            edges_list.append(source_index)
            edges_list.append(destination_index)
        except Exception as e:
            print(e, line)
# print("iter_cnt:", iter_cnt)
print("len(nodes_list)", len(nodes_list))
print("len(edges_list)", int(len(edges_list)/2))

hjson['nodes'] = nodes_list
hjson['edges'] = edges_list
hjson['dependentsCount'] = dependentsCount_list
# print(type(hjson))

# 生成json
with open("..\\000LocalData\\as_cn\\as_rel20200221_gao_cn.json", "w", encoding='utf-8') as f:
    json.dump(hjson, f)
    print("write json file complete!")

