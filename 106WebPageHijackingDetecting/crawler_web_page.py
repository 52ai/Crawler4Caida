# coding:utf-8
"""

create on Jul. 6, 2023 By Wayne YU
Email: ieeflsyu@outlook.com


Function:

一、整体需求
1、遍历国内网站列表，捕获网站首页截图、提取页面关键词（即指纹），存档。
2、每隔一段时间，重新抓取，并匹配，判断该网站是否存在网页劫持篡改的情况（需剔除其他原因，如网站故障、页面更新等）


二、已有基础
1、10million domains
2、IPIP地理定位库

三、整体思路
1、通过域名解析，拿到网站的IP地址，然后通过IPIP地理定位，判断其是否为国内；
2、对于国内的域名，抓取其首页截图、提取页面关键词（即指纹），然后存档；
3、每隔1天，重新抓取，然后逐一判断是否被劫持篡改。

按照上述思路，先出一个MVP（Minimum Viable Product）

"""



