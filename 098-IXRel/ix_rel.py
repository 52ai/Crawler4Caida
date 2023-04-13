# coding:utf-8
"""
create on Apr 8, 2023 By Wayne YU

Function:

统计全球通过IX产生的网络互联关系数量
根据https://www.peeringdb.com/api/netixlan
抽取ix和net的对应关系，依据AS接入的方式open或者selective，生成网络互联关系

"""

# from urllib.request import urlopen
import json
import time
import csv


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


def ix_view():
    """
    基于PEERING DB数据抽取ix和net对应关系，依据AS接入方式生成网络互联关系
    """
    # html = urlopen(r"https://www.peeringdb.com/api/netixlan")
    # html_json = json.loads(html.read())
    with open("./netixlan.json") as f:
        html_json = json.load(f)
    net_ix_result = []  # 存储网络接入IX的数据
    for item in html_json['data']:
        ix_id = item['ix_id']
        ix_name = item['name']
        asn = item['asn']
        is_rs_peer = item['is_rs_peer']
        temp_line = [ix_id, ix_name, asn, is_rs_peer]
        # print(temp_line)
        net_ix_result.append(temp_line)
    print(f"1、已成功统计{len(net_ix_result)}个AS-IX的接入关系")
    """
    基于AS-IX的接入关系，统计每个IX的接入AS，分为open_as_list、selective_as_list两组
    """
    ix2as_dict = {}  # 存储每个ix的接入as列表
    as_list = []  # 存储全球接入ix的AS列表
    for item in net_ix_result:
        ix_id = item[0]
        ix_name = item[1]
        asn = item[2]
        is_rs_peer = item[3]
        as_list.append(asn)
        if ix_id not in ix2as_dict.keys():
            ix2as_dict[ix_id] = {"ix_name": ix_name, "open": [], "selective": []}
            if is_rs_peer:
                ix2as_dict[ix_id]["open"].append(asn)
            else:
                ix2as_dict[ix_id]["selective"].append(asn)
        else:
            if is_rs_peer:
                ix2as_dict[ix_id]["open"].append(asn)
            else:
                ix2as_dict[ix_id]["selective"].append(asn)
    print(f"2、已提取处理全球{len(ix2as_dict)}个IX，这些IX均存在成员网络接入记录")
    print(f"3、已提出处理全球{len(set(as_list))}个AS，这些AS均存在IX接入记录, 占全球活跃自治域网络数量比：", round(len(set(as_list))/78000, 4))

    print("4、校验AMS-IX(26)的统计信息:",
          ix2as_dict[26]["ix_name"], "(name),",
          len(set(ix2as_dict[26]["open"])), "(open),",
          len(set(ix2as_dict[26]["selective"])), "(selective),",
          len(set(ix2as_dict[26]["open"]).union(set(ix2as_dict[26]["selective"]))), "(union)")

    print("5、遍历每个IX，统计通过该IX生成的网络互联关系数量")
    all_rel_cnt = 0
    all_rel_list = []
    for ix_id in ix2as_dict.keys():
        ix_name = ix2as_dict[ix_id]["ix_name"]
        open_cnt = len(set(ix2as_dict[ix_id]["open"]))
        selective_cnt = len(set(ix2as_dict[ix_id]["selective"]))
        union_cnt = len(set(ix2as_dict[ix_id]["open"]).union(set(ix2as_dict[ix_id]["selective"])))
        """
        网络互联关系生成规则如下：
        1）open接入的AS间两两间生成网络互联关系，然后按照网络互联关系对进行去重
        2）selective接入的AS，由于无法获知具体的互联方，暂不考虑
        """
        rel_cnt = (open_cnt * (open_cnt - 1))//2
        all_rel_cnt += rel_cnt

        temp_line = [ix_id, ix_name, open_cnt, selective_cnt, union_cnt, rel_cnt]
        print(temp_line)

        open_list = list(set(ix2as_dict[ix_id]["open"]))
        for i in range(0, len(open_list)):
            for j in range(i+1, len(open_list)):
                if int(open_list[i]) < int(open_list[j]):
                    all_rel_list.append(str(open_list[i]) + "-" + str(open_list[j]))
                else:
                    all_rel_list.append(str(open_list[j]) + "-" + str(open_list[i]))

    print("6、初步估算，通过全球IX生成的网络互联关系数量为：",
          all_rel_cnt, "(按“OPEN接入，两两互联”规则折算的全部关系对), ",
          len(set(all_rel_list)), "(去重后的结果)")
    print("7、将去重后的关系对，与全球RIB中as path观测到的关系对进行匹配，获取匹配成功的关系对数量")

    rel_file = "../000LocalData/as_relationships/serial-1/20230101.as-rel.txt"
    as_rel_cnt = 0  # 存储路由监测节点观测到的全球as rel数量
    as_rel_list = []  # 存储实际监测到的as关系
    with open(rel_file, "r", encoding="utf-8") as f:
        for line in f.readlines():
            if line.strip().find("#") == 0:
                continue
            line = line.strip().split("|")
            as_left = line[0]
            as_right = line[1]
            as_rel_cnt += 1
            if int(as_left) < int(as_right):
                as_rel_list.append(str(as_left)+"-"+str(as_right))
            else:
                as_rel_list.append(str(as_right)+"-"+str(as_left))
    print("1) 全球路由监测节点实际观测到的as rel数量：", len(as_rel_list))

    match_rel_list = set(all_rel_list).intersection(set(as_rel_list))
    print("2) 推断关系对与实际观测关系对相配的as rel数量：", len(match_rel_list), ", 占实际观测关系数量比：", round(len(match_rel_list)/len(as_rel_list), 4))
    match_rel_result = []
    for match_item in match_rel_list:
        match_item = match_item.strip().split("-")
        match_rel_result.append(match_item)
        # print(match_item)
    save_file = "./match_rel_result.csv"
    write_to_csv(match_rel_result, save_file)


if __name__ == "__main__":
    time_start = time.time()
    ix_view()
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
