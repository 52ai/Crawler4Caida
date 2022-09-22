# coding:utf-8
"""
create on Sep 22, 2022 By Wanye YU
Email: ieeflsyu@outlook.com

Function:
以悲惨世界数据集为样本，研究graphistry的可视化
"""
import pandas
import graphistry
links = pandas.read_csv('lesmiserables.csv')
print(links)

# 基础绑定
graphistry.register(api=3, username='ieeflsyu', password='go123456')
g = graphistry.bind(source="source", destination="target")

# 连边名称绑定
links["label"] = links.value.map(lambda v: "#rel type: %d" % v)
g = g.bind(edge_title="label")

g.edges(links).plot()
