# README 20200526
自俄罗斯断网事件分析任务开始，到Bird系统研究，再到CN-BGPMon原型开发计划的制定
通过不断学习前人的经验，对于CN-BGPMon原型的实现已经有了初步思路

在研究现有十多个经典BGP安全监测系统的基础上（公开系统 + 公开论文）
BGPMon(commercial): www.bgpmon.net<now>【控制平面】
ARTEMIS: Neutralising BGP Hijacking Within a Minute<2018>【控制平面】
Argus: An Accurate and Agile System to Detecting IP Prefix Hijacking<2012>【控制平面+数据平面】
HEAP: Reliable Assessment of BGP Hijacking Attacks<2016>【控制平面+数据平面】

PHAS: A Prefix Hijack Alter System<2006>【控制平面】
Cyclops: The AS-level Connectivity Observatory<2008>【控制平面】
iSpy: Detecting IP Prefix Hijacking on My Own<2008>【数据平面】
Zheng: A Light-Weight Distributed Scheme for Detecting  IP Prefix Hijacks in Real-Time<2007>【数据平面】
Hu: Accurate Real-time Identi_cation of IP Pre_x Hijacking<2007>【控制平面+数据平面】
Qiu&Gao: Detecting Bogus BGP Route Information:  Going Beyond Prefix Hijacking<2007>【控制平面】
Qiu: Locating Prefix Hijackers using LOCK<2009>【控制平面+数据平面】
Johann: A Forensic Case Study on AS Hijacking: The Attacker's Perspective<2013>【控制平面+数据平面】
大致理解了BGP安全事件的分类、BGP安全问题两类解决方案、第三方监测和AS自有监测系统实现难易程度、监测系统实现的多种途径

经研究CN-BGPMon的实现可借鉴Argus + BGPMon（Commercial）+ ARTEMIS + PHAS
其中Argus采用控制平面和数据平面混合的方式
而BGPMon(Commercial) 、ARTEMIS、PHAS均只采用控制平面信息

研究表明
只采用控制平面信息，其共同缺点是对前缀劫持识别的准确率较低。
由于多宿主、MOAS(Multiple Origin AS)、备份链路、BGP Anycast（如DNS解析服务器、IPv4/IPv6过渡以及CDN服务提供商）等各种复杂的情况
很难仅仅从控制层路由信息中准确判断一个路由改变是否是前缀劫持。

由于IP地址空间巨大，直接对全量IP前缀进行探测，会导致探测的时间成本和性能消耗巨大，不易于部署

因此可以把二者结合起来，先利用控制平面信息（如Prefix2AS、AS_PATH）发现异常事件，再利用数据层的探测信息去绘制事件指纹
最后通过指纹信息最终确认该异常事件是否为前缀劫持事件（包括前缀劫持、路由泄露）

下一步工作

1）构建Bird系统RIB和UPDATE MESSAGE报文的分析程序作为异常事件发现的原始数据。【自有监测能力】
2）构建RIPE NCC、RouteViews、BGPMon（live data）的UPDATE报文的实时接收和处理程序，以扩充路由监测的范围。【公开数据源】
3）构建Route-Server Telnet登录及操作程序，以获取数据层面的探测数据。
4）搜索公开资源并维护Route-Server列表（包括Telnet地址，登录用户名，登录密码），前人研究表明40个节点已能达到理想效果。
5）构建BGP路由安全事件核心识别引擎，对BGP前缀劫持（前缀和子前缀）、BGP路由泄露、BGP中断等事件进行监测
6）综合以上功能模块，形成CN-BGPMon原型系统。

以上便是对近期BGP安全态势感知系统研究的一个总结（已发邮件）
接下来的一个礼拜，可以全身心的投入到CN-BGPMon的实现过程中，争取在下礼拜的这个时候有一个初步的原型
后面再不断的迭代更新

那么一切就从Bird开始吧，把复杂系统结构成一个个简单的模块，逐一实现
1）bird_analysis.py
2）live_data_gain.py
3）data_probe.py
4）route_server.py
5）monitoring_engine.py
6）main.py