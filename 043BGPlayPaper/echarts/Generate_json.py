# coding:utf-8
"""
create on Sep 8, 2020 By Wayne YU
Function:

处理并生产相关json文件，用于生成Echarts

继续探索第二篇论文的可视化效果
"""

from urllib.request import urlopen
import json


time_str = "1999"

html = urlopen(r'http://static.popodv.com/data/attr/npmdep.json')
h_json = json.loads(html.read())

nodes_list = []
edges_list = []
dependentsCount_list = []

file_in = '..\\..\\000LocalData\\as_map\\as_core_map_data_new' + time_str + '1001.csv'
bgp_file = "..\\..\\000LocalData\\as_relationships\\serial-1\\" + time_str + "1001.as-rel.txt"

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

# print("len(map_asn2index):", len(map_asn2index))
# print(map_asn2index)

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
        pass


h_json['nodes'] = nodes_list
h_json['edges'] = edges_list
h_json['dependentsCount'] = dependentsCount_list

print(h_json)
print("时间:", time_str)
print("节点:", len(h_json['nodes']))
print("连边:", len(h_json['edges']) // 2)
# 生成json
save_path = "as_rel" + time_str + "1001.json"
with open(save_path, "w") as f:
    json.dump(h_json, f)
    print("write json file complete!")

