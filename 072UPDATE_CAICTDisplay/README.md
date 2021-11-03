create on Nov 3, 2021 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

院大屏数据要时常更新，紧要的有两部分数据，全球网络分布和全球互联网互联关系

1) 全球网络分布界面
   需要从RIPE或RouteViews公开数据源，提取v4和v6路由通告数据，然后结合先前的v4/v6统计程序，统计通告量
   关键还是统计每个AS v4和v6的通告量

2) 全球互联网互联关系界面
   主要是极图的绘制，依赖两个程序as_core_map_v3.py(生成as core map数据)和draw_as_core_v10.py（绘图）
   互联关系变化趋势依赖0_display_data.py
   外部互联关系依赖7_external_as_analysis_global.py程序
   全部互联关系依赖5_all_as_rel.py

   
先前对于高总的数据asn2ip和asn_info有依赖，此次更新后需要摆脱对二者的依赖，具体措施如下：
1) asn2ip文件，此文件可以暂时通过RIPE RRC00的路由表来解决，里面既有v4，也有v6
2) asn_info，则需要时常的通过as whois数据去维护（deal_as_org_info可以借助CAIDA维护一个还可以的asinfo信息）

