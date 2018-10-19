# coding:utf-8
"""
create on Oct 16,2018 by Wayne
using api get rank data
"""

import json
from urllib.request import urlopen


def count_AS(page_url_list):
    """
    以运营商为整体，对互联的AS号进行去重
    """
    cnt = 0
    as_list = []
    for page_url in page_url_list:
        response = urlopen(page_url).read().decode('utf-8')
        response_json = json.loads(response)
        response_json_item_list = response_json.get("data")
        # print(response_json_item_list)
        for item in response_json_item_list:
            if item.get("country") != "CN":
                as_list.append(item.get("asn"))
                # print(item.get("country"))
    # print("去重前计数：", len(as_list))
    as_list = list(set(as_list))
    # print("去重后计数：", len(as_list))
    print(as_list)
    return len(as_list)


if __name__ == "__main__":
    # url = "http://as-rank.caida.org/api/v1/asns/4134/links?populate=1"
    # print("TEST:", count_AS(url))
    """
    电信 AS号：4134、4089、49209、36678
    联通 AS号：4837、9929、10099、19174、197407
    移动 AS号：9808、58453、9231
    """
    dianxin_url_list = ["http://as-rank.caida.org/api/v1/asns/4134/links?populate=1",
                        "http://as-rank.caida.org/api/v1/asns/4809/links?populate=1",
                        "http://as-rank.caida.org/api/v1/asns/49209/links?populate=1",
                        "http://as-rank.caida.org/api/v1/asns/36678/links?populate=1"
                        ]
    liantong_url_list = ["http://as-rank.caida.org/api/v1/asns/4837/links?populate=1",
                         "http://as-rank.caida.org/api/v1/asns/9929/links?populate=1",
                         "http://as-rank.caida.org/api/v1/asns/10099/links?populate=1",
                         "http://as-rank.caida.org/api/v1/asns/19174/links?populate=1",
                         "http://as-rank.caida.org/api/v1/asns/197407/links?populate=1"
                        ]
    yidong_url_list = ["http://as-rank.caida.org/api/v1/asns/9808/links?populate=1",
                       "http://as-rank.caida.org/api/v1/asns/58453/links?populate=1",
                       "http://as-rank.caida.org/api/v1/asns/9231/links?populate=1"
                       ]

    """
        cnt_isp = 0
    for as_url in dianxin_url_list:
        temp_cnt = count_AS(as_url)
        print(as_url, ":", temp_cnt)
        cnt_isp += temp_cnt
    print("电信AS总计数:", cnt_isp)

    cnt_isp = 0
    for as_url in liantong_url_list:
        temp_cnt = count_AS(as_url)
        print(as_url, ":", temp_cnt)
        cnt_isp += temp_cnt
    print("联通AS总计数:", cnt_isp)

    cnt_isp = 0
    for as_url in yidong_url_list:
        temp_cnt = count_AS(as_url)
        print(as_url, ":", temp_cnt)
        cnt_isp += temp_cnt
    print("移动AS总计数:", cnt_isp)
    
    """
    print("电信AS总计数:", count_AS(dianxin_url_list))
    print("联通AS总计数:", count_AS(liantong_url_list))
    print("移动AS总计数:", count_AS(yidong_url_list))

