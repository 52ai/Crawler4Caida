## Crawler4Caida
>Repository:Crawler4Caida<br>
>Author:Wayne Yu<br>
>Date: 19 Oct 2018<br>
>Description:一个致力于用Python提高部门工作自动化水平的程序库！（包括网络数据爬取、办公自动化、辅助研究等）<br>
>

一个关于CAIDA网络研究数据爬取的爬虫程序库，包括全球AS、DNS、IPV4/IPV6等。--2018.10.19 By Wayne Yu<br>
始于CAIDA，而不止于CAIDA！未来此库就会有更多的可能性Using Python3.X！---2019.04.05 By Wayne Yu<br>
懒得再去建库了，入职后所有的Python程序都扔这里面了。--2019.05.08 By Wayne Yu<br>
修改仓库的Description为：一个致力于用Python提高部门工作自动化水平的程序库！（包括网络数据爬取、办公自动化、辅助研究等）--- 2019.05.09 By Wayne Yu<br>
尝试着坚持每天Github，坚持每天写点程序，老本行不能丢！今天是Github连击第4天，加油！---2019..05.11 By Wayne Yu<br>
## 关于CAIDA
Founded in 1997, the Center for Applied Internet Data Analysis (CAIDA) conducts network research and builds research infrastructure to support large-scale data collection, curation, and data distribution to the scientific research community.<br>
CAIDA（the Center for Applied Internet Data Analysis），中文全称为互联网应用数据分析中心，引导网络研究并构建网络研究基础设施，为大规模的数据采集、管理，并将数据分发至科学研究社区提供支撑。<br>
详细信息可以通过这个2页的PDF获取：[下载](http://www.caida.org/publications/posters/eps/caida-infosheet-2016.pdf)<br>

**CAIDA的使命**<br>
```
1）provide macroscopic insights into Internet infrastructure, behavior, usage, and evolution,
2）foster a collaborative environment in which data can be acquired, analyzed, and (as appropriate) shared,
3）improve the integrity of the field of Internet science,
4）inform science, technology, and communications public policies.
```
About CAIDA还有[Annual Report](http://www.caida.org/home/about/annualreports/)、[Program Plan](http://www.caida.org/home/about/progplan/)、[Institutional Review Board（IRB）Approval Process](http://www.caida.org/home/about/irb/) 、[About CAIDA Staff](http://www.caida.org/home/staff/)。
## 为什么要建Crawler4Caida开源库

因部门工作内容需要，在研究的过程中会用到CAIDA数据中心中的网络数据，并对其进行一定的处理分析，按需求提取结果。在编写爬虫的过程中发现，虽然每次具体的需求不一，但是抓取数据的思路大同小异。<br>
为提供高工作效率，减少不必要的开发成本，特建此库，把以往编写Caida网络数据爬虫记录下来，并通过后期的程序重构和新需求的加入，以不断充实此开源库。

## Crawler4Caida库结构

automation --- 按照任务以文件夹的形式进行管理源程序<br>
crawler --- 放置按需求编写的爬虫程序，一般是以单个文件的形式存档<br>
crawler4caida --- 不定期更新系统化的CAIDA数据的分析程序，不限于AS号、DNS、IPv4/IPv6、网间互联互通等内容<br>
refactoring --- 放置重构之后的爬虫程序，一般完成时间较晚<br>
requirements.md  ---需求记录文档<br>
README.md  ---库介绍文档<br>

## MORE

更多的信息可以访问，[云中布衣](http://www.mryu.top/)搜索Crawler4Caida进行留言讨论。