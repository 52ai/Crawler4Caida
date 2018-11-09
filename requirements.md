## 需求列表

#### 20181016
**需求**：按要求分电信、移动、联通，统计AS Rank数量。爬取页面连接如下所示：<br>

**中国电信**<br>

[http://as-rank.caida.org/asns/?name=4134&type=search](http://as-rank.caida.org/asns/?name=4134&type=search)<br>
[http://as-rank.caida.org/asns/?name=4809&type=search](http://as-rank.caida.org/asns/?name=4809&type=search)<br>
[http://as-rank.caida.org/asns/?name=49209&type=search](http://as-rank.caida.org/asns/?name=49209&type=search)<br>
[http://as-rank.caida.org/asns/?name=36678&type=search](http://as-rank.caida.org/asns/?name=36678&type=search)

**中国联通**<br>

[http://as-rank.caida.org/asns/?name=4837&type=search](http://as-rank.caida.org/asns/?name=4837&type=search)<br>
[http://as-rank.caida.org/asns/?name=9929&type=search](http://as-rank.caida.org/asns/?name=9929&type=search)<br>
[http://as-rank.caida.org/asns/?name=10099&type=search](http://as-rank.caida.org/asns/?name=10099&type=search)<br>
[http://as-rank.caida.org/asns/?name=19174&type=search](http://as-rank.caida.org/asns/?name=19174&type=search)<br>
[http://as-rank.caida.org/asns/?name=197407&type=search](http://as-rank.caida.org/asns/?name=197407&type=search)

**中国移动**<br>
[http://as-rank.caida.org/asns/?name=9808&type=search](http://as-rank.caida.org/asns/?name=9808&type=search)<br>
[http://as-rank.caida.org/asns/?name=58453&type=search](http://as-rank.caida.org/asns/?name=58453&type=search)<br>
[http://as-rank.caida.org/asns/?name=9231&type=search](http://as-rank.caida.org/asns/?name=9231&type=search)<br>

统计每个链接中，除去中国后，As Rank的数量，并按运营商去重汇总。<br>
原计划使用selenium+phantomJS的方式爬取动态页面，并提取出有效的信息，后面因为windows环境的问题，导致该方法一直无法成功，最后直接找到获取数据的API接口，获取了相关数据并按要求处理完毕。<br>
后续有时间再尝试下动态页面的爬取方案。<br>

**实现文件**：[crawler/crawler_task_1.py](https://github.com/52ai/Crawler4Caida/blob/master/crawler/CT001.py)

