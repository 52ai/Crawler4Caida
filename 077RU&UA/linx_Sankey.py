# coding:utf-8
"""
create on Mar 25, 2022 By Wayne YU

Function:

借助桑基图构建，俄网络通过全球交换中心去往全球网络的依赖关系，并绘制LINX事件的前后影响

分三列
某俄网络，某全球IX，全球其他网络
"""
import json
import time
import csv

from pyecharts import options as opts
from pyecharts.charts import Sankey
from pyecharts.globals import ThemeType


except_info_list = []  # 存储异常


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return None:
    """
    print("write file<%s> ..." % des_path)
    csv_file = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csv_file, delimiter=",")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
    print("write finish!")


def gain_as2country_caida():
    """
    根据Caida asn info获取as对应的国家信息
    :return as2country:
    """
    as_info_file = '..\\000LocalData\\as_Gao\\asn_info_from_caida.csv'
    as2country = {}  # 存储as号到country的映射关系
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split(",")
        # print(line)
        as_number = line[0]
        as_country = line[-1]
        as2country[as_number] = as_country
    return as2country


def gain_as2info_pdb():
    """
    根据pdb的数据获取as 2 info的信息
    https://www.peeringdb.com/api/net
    :return as2info:
    """
    with open("../000LocalData/IXVis/net.json") as json_file:
        html_json = json.load(json_file)
    as2info = {}  # as2info的字典
    for item in html_json['data']:
        asn = item["asn"]
        name = item["name"]
        if asn not in as2info.keys():
            as2info[asn] = name
    # print("NET原始信息记录：", len(html_json['data']))
    print("AS信息字典记录：", len(as2info.keys()))
    return as2info


def gain_ix2info_pdb():
    """
    根据pdb的数据获取ix 2 info的信息
    https://www.peeringdb.com/api/ix
    :return ix2info:
    """
    with open("../000LocalData/IXVis/ix.json") as json_file:
        html_json = json.load(json_file)
    ix2info = {}  # ix2info的字典
    for item in html_json['data']:
        ix_id = item['id']
        ix_name = item['name']
        ix_name_long = item['name_long']
        city = item['city']
        country = item['country']
        region = item['region_continent']
        net_count = item['net_count']
        fac_count = item['fac_count']
        if ix_id not in ix2info.keys():
            ix2info[ix_id] = [ix_name, ix_name_long, city, country, region, net_count, fac_count]
    # print("IX原始信息记录表：", len(html_json['data']))
    print("IX信息字典记录：", len(ix2info.keys()))
    return ix2info


def ix_sankey_view():
    """
    基于PEERING DB数据抽取ix和net对应关系
    构建俄网络，全球IX，全球网络，三大集合，通过sankey图可是换LINX事件前后的变化
    https://www.peeringdb.com/api/netixlan
    nodes = [
        {"name": "category1"},
        {"name": "category2"},
        {"name": "category3"},
        {"name": "category4"},
        {"name": "category5"},
        {"name": "category6"},
    ]

    links = [
        {"source": "category1", "target": "category2", "value": 10},
        {"source": "category2", "target": "category3", "value": 15},
        {"source": "category3", "target": "category4", "value": 20},
        {"source": "category5", "target": "category6", "value": 25},
    ]
    :return:
    """
    as2info = gain_as2info_pdb()
    ix2info = gain_ix2info_pdb()
    as2country_dict = gain_as2country_caida()

    nodes = []  # 存储绘图节点
    links = []  # 存储绘图关系
    """
    节点包括三类，俄罗斯网络、全球IX、全球网络
    """
    with open("netixlan.json") as json_file:
        html_json = json.load(json_file)

    for item in html_json['data']:
        """
        {'id': 38, 
        'net_id': 2, 
        'ix_id': 13, 
        'name': 'SIX Seattle: MTU 1500', 
        'ixlan_id': 13, 
        'notes': '', 
        'speed': 200000, 
        'asn': 20940, 
        'ipaddr4': '206.81.80.113', 
        'ipaddr6': '2001:504:16::51cc', 
        'is_rs_peer': False, 
        'operational': True, 
        'created': '2010-07-29T00:00:00Z', 
        'updated': '2020-02-12T14:34:55Z', 
        'status': 'ok'} 
        基于IX NAME构建主要IX的接入关系
        """
        if item['name'].find("LINX") == -1:
            continue
        ix_id = item['ix_id']
        ix_name = item['name'].strip().split(":")[0]
        ix_sankey = "IX" + str(ix_id) + "-"+ix_name

        asn = item['asn']
        print(asn)
        try:
            asn_str = as2info[asn]
        except Exception as e:
            except_info_list.append(e)
            asn_str = "UNKnow"
        asn_sankey = "AS"+str(asn)+"-"+asn_str

        asn_country = "ZZ"
        try:
            asn_country = as2country_dict[str(asn)]
        except Exception as e:
            except_info_list.append(e)
        print(asn_country)

        print(ix_sankey, " ", asn_sankey)

        ix_node = {"name": ix_sankey}
        asn_node = {"name": asn_sankey}

        if asn_country == "RU":
            rel_temp = {"source": asn_sankey, "target": ix_sankey, "value": 0.1}
            links.append(rel_temp)

            if ix_node not in nodes:
                nodes.append(ix_node)
            if asn_node not in nodes:
                nodes.append(asn_node)

        elif asn_country == "CN":
            rel_temp = {"source": ix_sankey, "target": asn_sankey, "value": 0.1}
            links.append(rel_temp)

            if ix_node not in nodes:
                nodes.append(ix_node)
            if asn_node not in nodes:
                nodes.append(asn_node)

    draw_sankey(nodes, links)


def draw_sankey(nodes, links):
    """
    根据传入的nodes和links，构建sankey图
    :param nodes:
    :param links:
    :return:
    """
    c = (
        Sankey(init_opts=opts.InitOpts(width="1900px",
                                       height="900px",
                                       page_title="Sankey",
                                       theme=ThemeType.ROMA))
        .add(
            "sankey",
            nodes,
            links,
            # orient="vertical",
            linestyle_opt=opts.LineStyleOpts(opacity=0.2, curve=0.5, color="source"),
            label_opts=opts.LabelOpts(position="top"),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="Sankey-RU&IX&Global"))
        .render("sankey_ru_ix.html")
    )


if __name__ == "__main__":
    time_start = time.time()
    ix_sankey_view()
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
