# coding:utf-8
"""
create on July 4, 2021 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

抽取交换中心到网络间的关系，以供星云图绘制使用

思路：
直接通过https://www.peeringdb.com/api/netixlan
抽取ix和net的对应关系，即每个ix都有哪些网络接入

形成ix组，net组，以及ix-net的关系

"""