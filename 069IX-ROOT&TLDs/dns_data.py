# coding: utf-8
"""
create on Oct 13, 2021 By Wenyan YU

Function:

为进一步分析Root Servers和TLDs与IX的关系，需要深入研究根域名服务器和顶级域的所属网络数据
1)root servers数据由于只有13个，手动处理就可以
2)TLDs大概有1495个，每个顶级域可能会有多个IP，需要对这些数据进行爬取，并将IP转换为AS网络，才可与IX-AS数据进行整合
"""

