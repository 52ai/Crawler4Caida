# coding:utf-8
"""
create on Oct 19,2018 by Wayne
refactor crawler for CAIDA
"""

import json
from urllib.request import urlopen


def get_info(page_url):
    """
    通过API获取AS Links的相关信息
    """
    response = urlopen(page_url).read().decode('utf-8')
    response_json = json.loads(response)
    response_json_item_list = response_json.get("data")
    print(response_json_item_list)


if __name__ == "__main__":
    # url = "http://as-rank.caida.org/api/v1/asns/4134/links?populate=1"
    # print("TEST:", count_AS(url))
    """
    电信 AS号：4134、4089、49209、36678
    联通 AS号：4837、9929、10099、19174、197407
    移动 AS号：9808、58453、9231
    
    以电信4314 AS号为例，其API接口为：http://as-rank.caida.org/api/v1/asns/4134/links?populate=1
    """
    api_url = "http://as-rank.caida.org/api/v1/asns/4134/links?populate=1"
    get_info(api_url)

