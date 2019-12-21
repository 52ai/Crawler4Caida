# coding:utf-8
"""
create on Dec 8, 2019 By Wayne YU
Function:

处理并生产相关json文件，用于生成Echarts
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

# for item in range(0, 10000):
#     str_as = "AS" + str(item)
#     nodes_list.append(str_as)
#
#
# for item in range(0, 9999):
#     edges_list.append(item)
#     edges_list.append(item + 1)
#
# for item in range(0, 10000):
#     dependentsCount_list.append(1)

file_in = '..\\000LocalData\\as_map\\as_core_map_data_new20001001.csv'
bgp_file = "..\\000LocalData\\as_relationships\\serial-1\\20001001.as-rel.txt"

file_read = open(file_in, 'r', encoding='utf-8')
map_asn2index = {}
asn_index = 0
asn_temp = ""
for line in file_read.readlines():
    line = line.strip().split('|')
    if len(line) < 11:
        continue
    if asn_temp == line[0]:
        continue
    nodes_str = line[5] + "(AS"+line[0]+")"
    nodes_list.append(nodes_str)
    dependentsCount_list.append(int(line[1]))
    map_asn2index[line[0]] = asn_index
    asn_index += 1
    asn_temp = line[0]

print("len(map_asn2index):", len(map_asn2index))
print(map_asn2index)

"""
在上面的循环中，需要建立ASN与index Number的对应关系
"""

bgp_file_read = open(bgp_file, 'r', encoding='utf-8')
for line in bgp_file_read.readlines():
    if line.strip().find("#") == 0:
        continue
    line = line.strip().split('|')
    # print(line)
    try:
        source_index = map_asn2index[line[0]]
        destination_index = map_asn2index[line[1]]
        # print(source_index, destination_index)
        edges_list.append(source_index)
        edges_list.append(destination_index)
    except Exception as e:
        print(e, line)


hjson['nodes'] = nodes_list
hjson['edges'] = edges_list
hjson['dependentsCount'] = dependentsCount_list
print(type(hjson))

# 生成json
with open("../000LocalData/as_echarts/as_rel20001001.json", "w") as f:
    json.dump(hjson, f)
    print("write json file complete!")

