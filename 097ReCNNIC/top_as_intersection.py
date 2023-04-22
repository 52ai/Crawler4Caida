# coding:utf-8
"""
create on Apr 21, 2023 By Wayne YU

Function: 统计两个口径TOP AS的交集

"""
cn_topn_as_list = []
cnt = 1
with open("../000LocalData/ReCNNIC/cn_as.csv", "r", encoding="gbk") as f:
    for item in f.readlines():
        item = item.strip().split(",")
        asn = item[1].strip("AS")
        cn_topn_as_list.append(asn)
        if cnt >= 100:
            break
        cnt += 1
print("CAICT TOP 100：", cn_topn_as_list)

cn_topn_as_list_cnnic = []

cnt = 1
with open("../000LocalData/ReCNNIC/cn_as_cnnic.csv", "r", encoding="utf-8") as f:
    for item in f.readlines():
        item = item.strip().split(",")
        asn = item[0]
        cn_topn_as_list_cnnic.append(asn)
        if cnt >= 100:
            break
        cnt += 1
print("CNNIC TOP 100:", cn_topn_as_list_cnnic)

top_as_intersection = set(cn_topn_as_list).intersection(set(cn_topn_as_list_cnnic))
print("重合：", top_as_intersection, "\n数量:", len(top_as_intersection))
