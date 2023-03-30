# coding:utf-8
"""
create on Mar 29, 2023 By Wayne YU

Function:

针对CNNIC的数据做回应分析
CN TOP100 AS（按IPv4地址数量排名）间的通路：通过三大运营商骨干网RIB，获取全部路径，然后进一步分析国外绕转的情况

"""
import time
import csv
# from IPy import IP


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return: None
    """
    print("write file <%s> ..." % des_path)
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


def gain_as2org_caida():
    """
    根据Caida asn info获取as对应的org信息
    :return as2country:
    """
    as_info_file = '..\\000LocalData\\as_Gao\\asn_info_from_caida.csv'
    as2org_dic = {}  # 存储as号到country的映射关系
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split(",")
        # print(line)
        as_number = line[0]
        as_org = line[2] + "," + line[1]
        as2org_dic[as_number] = as_org
    return as2org_dic


def gain_cn_topn_as(topn):
    """
    根据IPv4地址量排名，获取cn top n自治域列表
    :param topn:
    :return cn_topn_as_list:
    """
    cn_topn_as_list = []
    cnt = 1
    with open("../000LocalData/ReCNNIC/cn_as.csv", "r", encoding="gbk") as f:
        for item in f.readlines():
            item = item.strip().split(",")
            asn = item[1].strip("AS")
            cn_topn_as_list.append(asn)
            if cnt >= topn:
                break
            cnt += 1
    return cn_topn_as_list


def rib_analysis(rib_file):
    """
    分析RIB数据，统计两端都是国内，中间有出国的情况
    :param rib_file:
    :return:
    """
    as2country_dic = gain_as2country_caida()
    as2org_dic = gain_as2org_caida()
    left_as_list = ["4134", "4837", "9808"]
    cn_top100_as_list = gain_cn_topn_as(100)  # 获取CN TOP 100的列表

    """
    把移动AS58453、联通AS10099、电信AS23764，纳入统计范畴
    """

    # cn_top100_as_list.append("58453")
    # cn_top100_as_list.append("10099")
    # cn_top100_as_list.append("23764")

    # print("CN TOP100 AS:", cn_top100_as_list)
    # print("AS4134's Country:", as2country_dic['4134'])

    file_read = open(rib_file, 'r', encoding='utf-8')
    all_prefix_num = 0  # 统计国内节点采集到的全部路由条目
    internal_prefix_list = []  # 统计国内节点采集到的两端都在国内的路由条目
    bypass_abroad = []  # 统计两端在国内，中间经过国外的路由前缀及AS PATH
    bypass_abroad_prefix_list = []  # 统计两端在国内，中间经过国外的路由前缀

    all_as_path_list = []  # 存储限定条件节点集合间所有的路径
    bypass_abroad_as_path_list = []  # 限定条件节点集合间所有路径中经过国际的路径

    except_info_list = []  # 存储异常记录信息
    for line in file_read.readlines():
        line = line.strip().split("|")
        v4_prefix = line[5]
        as_path = line[-2].split(" ")
        if str(v4_prefix).find("0.0.0.0/0") != -1:
            # 剔除全零路由
            # print(v4_prefix)
            continue
        all_prefix_num += 1
        # left_country = "ZZ"
        # right_country = "ZZ"

        # try:
        #     left_country = as2country_dic[str(as_path[0])]
        #     right_country = as2country_dic[str(as_path[-1])]
        # except Exception as e:
        #     except_info_list.append(e)

        if str(as_path[0]) in left_as_list and str(as_path[-1]) in cn_top100_as_list:  # 找出CN top100 AS间的总的路由路径
            internal_prefix_list.append(v4_prefix)
            all_as_path_list.append(str(as_path))
            for item_as in as_path[1:-1]:  # 遍历as path，获取每一跳的国别
                temp_country = "ZZ"
                try:
                    temp_country = as2country_dic[str(item_as)]
                except Exception as e:
                    except_info_list.append(e)

                if temp_country == "":
                    temp_country = "ZZ"

                # if item_as in ["37963", "58453", "10099", "23764", "36678"]:  # 阿里的US网络，不算出国绕
                if item_as in ["37963"]:  # 阿里的US网络，不算出国绕
                    temp_country = "CN"

                if temp_country != "CN" and temp_country != "ZZ":  # 找出中间出境绕的路

                    right_as_org = "ZZ"  # 获取源AS的机构信息
                    try:
                        right_as_org = as2org_dic[str(as_path[-1])]
                    except Exception as e:
                        except_info_list.append(e)

                    # print(v4_prefix, as_path, temp_country, as_path[-1], right_as_org)
                    bypass_abroad.append([v4_prefix, as_path[0], as_path, item_as, temp_country, as_path[-1], right_as_org])
                    bypass_abroad_prefix_list.append(v4_prefix)
                    bypass_abroad_as_path_list.append(str(as_path))
                    break

    print("三家运营商骨干网采集路由总数：", all_prefix_num)
    print("CN TOP100 AS间的路由路径数量:", len(all_as_path_list), "——去重后：", len(set(all_as_path_list)))
    print("CN TOP100 AS间经境外绕转的路由路径数量：", len(bypass_abroad_as_path_list), "——去重后:", len(set(bypass_abroad_as_path_list)))

    print("CN TOP100 AS间经境外绕转的路由路径数量（去重后）占比：", len(set(bypass_abroad_as_path_list))/len(set(all_as_path_list)))
    print("CN TOP100 AS间经境外绕转的路由路径数量占比：", len(bypass_abroad_as_path_list) / len(all_as_path_list))

    print("------开展三家加权统计（按照路径去重）---------")
    all_cnt_dic = {}
    for item_path in set(all_as_path_list):
        item_path = item_path.strip("[").strip("]").strip().split(",")
        # print(item_path[0])
        if item_path[0] not in all_cnt_dic.keys():
            all_cnt_dic[item_path[0]] = 1
        else:
            all_cnt_dic[item_path[0]] += 1
    print("all_cnt_dict:", all_cnt_dic)

    bypass_cnt_dic = {}
    for item_path in set(bypass_abroad_as_path_list):
        item_path = item_path.strip("[").strip("]").strip().split(",")
        # print(item_path[0])
        if item_path[0] not in bypass_cnt_dic.keys():
            bypass_cnt_dic[item_path[0]] = 1
        else:
            bypass_cnt_dic[item_path[0]] += 1
    print("bypass_cnt_dict:", bypass_cnt_dic)

    # 运营商top100，电信：61个，联通：18个，移动：21个
    bypass_weight = 0
    if len(bypass_cnt_dic.keys()) != 0:
        bypass_weight = int(bypass_cnt_dic["'4134'"]) * 61 + int(bypass_cnt_dic["'4837'"]) * 18 + int(bypass_cnt_dic["'9808'"]) * 21
    all_weight = int(all_cnt_dic["'4134'"]) * 61 + int(all_cnt_dic["'4837'"]) * 18 + int(all_cnt_dic["'9808'"]) * 21
    print("bypass_weight:", bypass_weight)
    print("all_weight:", all_weight)
    print("下游加权统计的占比：", bypass_weight/all_weight)

    print("------开展三家加权统计（不去重）---------")
    all_cnt_dic = {}
    for item_path in all_as_path_list:
        item_path = item_path.strip("[").strip("]").strip().split(",")
        # print(item_path[0])
        if item_path[0] not in all_cnt_dic.keys():
            all_cnt_dic[item_path[0]] = 1
        else:
            all_cnt_dic[item_path[0]] += 1
    print("all_cnt_dict:", all_cnt_dic)

    bypass_cnt_dic = {}
    for item_path in bypass_abroad_as_path_list:
        item_path = item_path.strip("[").strip("]").strip().split(",")
        # print(item_path[0])
        if item_path[0] not in bypass_cnt_dic.keys():
            bypass_cnt_dic[item_path[0]] = 1
        else:
            bypass_cnt_dic[item_path[0]] += 1
    print("bypass_cnt_dict:", bypass_cnt_dic)

    # 运营商top100，电信：61个，联通：18个，移动：21个
    bypass_weight = 0
    if len(bypass_cnt_dic.keys()) != 0:
        bypass_weight = int(bypass_cnt_dic["'4134'"]) * 61 + int(bypass_cnt_dic["'4837'"]) * 18 + int(bypass_cnt_dic["'9808'"]) * 21
    all_weight = int(all_cnt_dic["'4134'"]) * 61 + int(all_cnt_dic["'4837'"]) * 18 + int(all_cnt_dic["'9808'"]) * 21
    print("bypass_weight:", bypass_weight)
    print("all_weight:", all_weight)
    print("下游加权统计的占比：", bypass_weight/all_weight)

    save_file = "..\\000LocalData\\ReCNNIC\\bypass_abroad.csv"
    write_to_csv(bypass_abroad, save_file)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    rib_analysis("..\\000LocalData\\BGPData\\rib_live\\rib_2023-01-13_181.txt")
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
