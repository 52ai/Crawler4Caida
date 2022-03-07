# coding:utf-8
"""
create on Jun 2, 2021 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

对6号节点的RIB数据进行处理，提取出电信、移动、联通以及HangZhouIX的BGP数据，并开展相关分析
这个分析很有意义，可形成实时报告机制
"""
import time
import csv
from IPy import IP

rib_file = "..\\000LocalData\\RU&UA\\rib\\z0224.txt"
as_info_file = '../000LocalData/as_Gao/asn_info.txt'
country_info_file = '../000LocalData/as_geo/GeoLite2-Country-Locations-zh-CN.csv'


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return: None
    """
    # print("write file <%s> ..." % des_path)
    csv_file = open(des_path, 'w', newline='', encoding='gbk')
    try:
        writer = csv.writer(csv_file, delimiter=",")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
    # print("write finish!")


def gain_as2country():
    """
    根据as info file信息获取AS与国家的对应字典
    :return as2country:
    :return as2info:
    """
    as2country = {}  # 存储as号到country的映射关系
    as2info = {}  # 存储as号到info的映射关系
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("\t")
        as_number = line[0]
        as_country = line[1].strip().split(",")[-1].strip()
        as2country[as_number] = as_country
        as2info[as_number] = line[1]
    return as2country, as2info


def gain_country2info():
    """
    根据country的缩写，获取其所在大洲及中文名信息
    :return country2continent:
    :return country2name:
    """
    country2continent = {}  # 存储国家到大洲的信息
    country2name = {}  # 存储国家缩写到国家名称的信息
    file_read = open(country_info_file, 'r', encoding='gbk')
    for line in file_read.readlines():
        line = line.strip().split(",")
        # print(line)
        country_ab = line[4]
        country_name = line[5]
        country_continent = line[3]
        country2continent[country_ab] = country_continent
        country2name[country_ab] = country_name
    return country2continent, country2name


def rib_analysis_table_dump2(asn, rib_list):
    """
    TABLE_DUMP2类型的RIB表处理分析
    根据传入的asn及其rib list，开展相关分析
    :param asn:
    :param rib_list:
    :return:
    """
    as2country, as2info = gain_as2country()
    country2continent, country2name = gain_country2info()
    print("= = = = = = = = =TABLE_DUMP2 RIB 详细分析= = = = = = = ")
    print("RIB来源: AS"+asn)
    print("RIB总的记录数：", len(rib_list))
    """
    针对每个RIB可以做很详细的分析：
    1）现网活跃AS网络，按国家、大洲维度进行统计分析。
    2）现网通告路由前缀以及IPv4地址数量，按AS网络、国家、大洲维度进行统计分析。
    3）AS网络间的互联关系分析。
    4）我国国际路由获取依赖关系分析。
    5）网络仿真实验。
    """

    print("- - - - -1)现网活跃AS网络，按照国家、大洲维度进行统计分析- - - ")
    active_as = []  # 存储全球活跃的AS数量
    for line in rib_list:
        line_as = line[1].split(" ")
        for item in line_as:
            if item.find("{") == -1:
                active_as.append(item)
            else:
                """
                存在特殊情况，AS6412及AS42781、AS201378均通告了168.187.247.0/24前缀
                168.187.247.0/24|4134 3356 59605 42961 42961 6412 {42781,201378}|IGP
                168.187.247.0/24|9808 58453 3356 59605 42961 42961 6412 {42781,201378}|IGP
                168.187.247.0/24|4837 1299 59605 42961 42961 6412 {42781,201378}|INCOMPLETE
                """
                item.strip("{").strip("}").split(",")
                active_as.extend(item)
    active_as = list(set(active_as))
    print("现网活跃AS网络数量：", len(active_as))
    country_as_dict = {}  # 以国家作为key，统计活跃as网络数量
    except_as = []  # 存储没有信息的AS列表
    for item_as in active_as:
        item_as_country = "ZZ"
        try:
            item_as_country = as2country[item_as]
        except Exception as e:
            # print(e)
            except_as.append(e)  # 记录没有信息的AS列表
        if item_as_country not in country_as_dict.keys():
            country_as_dict[item_as_country] = [item_as]
        else:
            country_as_dict[item_as_country].append(item_as)
    print("国家key数量:", len(country_as_dict.keys()))
    print("Except AS 记录数量：", len(except_as))
    print("现网活跃AS网络数量（中国）:", len(country_as_dict["CN"]))
    print("现网活跃AS网络数量（美国）:", len(country_as_dict["US"]))
    print("现网活跃AS网络数量（巴西）:", len(country_as_dict["BR"]))

    continent_as_dict = {}  # 存储某个大洲的AS
    except_as = []  # 存储异常的记录
    for item_as in active_as:
        try:
            item_as_country = as2country[item_as]
            item_as_continent = country2continent[item_as_country]
        except Exception as e:
            # print(e)
            item_as_continent = "查无"
            except_as.append(e)  # 记录没有信息的AS列表

        if item_as_continent not in continent_as_dict.keys():
            continent_as_dict[item_as_continent] = [item_as]
        else:
            continent_as_dict[item_as_continent].append(item_as)
    print("大洲key数量:", len(continent_as_dict.keys()))
    print("Except AS 记录数量：", len(except_as))
    for item_key in continent_as_dict.keys():
        print("大洲："+item_key,
              ", 活跃AS数量:"+str(len(continent_as_dict[item_key])),
              ", 占比："+str((len(continent_as_dict[item_key])/len(active_as))))
    print("- - - - -2)现网通告路由前缀以及IPv4地址数量，按AS网络、国家、大洲维度进行统计分析- - - ")
    as2prefix_dict = {}  # 统计每个AS通告的IP地址前缀
    for line in rib_list:
        line_prefix = line[0]
        if line[1].find("{") == -1:
            line_as = line[1].split(" ")
            origin_as = line_as[-1]
        else:
            line_as = line[1].split(" ")
            origin_as = line_as[-2]
        # print(line_prefix, origin_as)
        if origin_as not in as2prefix_dict.keys():
            as2prefix_dict[origin_as] = [line_prefix]
        else:
            as2prefix_dict[origin_as].append(line_prefix)
    print("AS key数量：", len(as2prefix_dict.keys()))
    as7018_ipv4_num = 0
    for ipv4_prefix in as2prefix_dict["7018"]:
        as7018_ipv4_num += len(IP(ipv4_prefix))
    print("AS7018(AT&T) IPv4前缀规模:%s, IPv4地址数量：%s" % (len(as2prefix_dict["7018"]), as7018_ipv4_num))

    as4134_ipv4_num = 0
    for ipv4_prefix in as2prefix_dict["4134"]:
        as4134_ipv4_num += len(IP(ipv4_prefix))
    print("AS4134(中国电信) IPv4前缀规模:%s, IPv4地址数量：%s" % (len(as2prefix_dict["4134"]), as4134_ipv4_num))

    global_prefix = 0
    global_ipv4_num = 0
    global_ipv4_num_list = []  # 存储去重的ipv4地址
    for as_key in as2prefix_dict.keys():
        for prefix_item in as2prefix_dict[as_key]:
            global_prefix += 1
            global_ipv4_num += len(IP(prefix_item))

    print("全球 IPv4前缀规模:%s, IPv4地址数量:%s, IPv4地址数量（去重）:%s" % (global_prefix, global_ipv4_num, len(global_ipv4_num_list)))
    print("- - - - -3)AS网络间的互联关系分析- - - ")
    print("即商业关系推断算法，需结合空间和时间维度数据")
    print("- - - - -4)我国国际路由分析- - - ")
    print("此处是我国互联网流量流向模型的关键")
    direct_as2prefix_dict = {}  # 存储直联as网络的prefix
    for line in rib_list:
        line_prefix = line[0]
        if line[1].find("{") == -1:
            line_as_path = line[1].split(" ")
        else:
            line_as_path = line[1].split(" ")[0:-1]
        # print(line_prefix, line_as_path)
        if len(line_as_path) == 1:
            pass
        else:
            direct_as = line_as_path[1]
            # print(direct_as, line_prefix)
            if direct_as not in direct_as2prefix_dict.keys():
                direct_as2prefix_dict[direct_as] = [line_prefix]
            else:
                direct_as2prefix_dict[direct_as].append(line_prefix)
    print("Direct AS Key数量：", len(direct_as2prefix_dict.keys()))
    direct_country_as_dict = {}  # 以国家作为key，统计直联网络数量、prefix数量及IP地址数量
    except_as = []  # 存储没有信息的AS列表
    for item_as in direct_as2prefix_dict.keys():
        item_as_country = "ZZ"
        try:
            item_as_country = as2country[item_as]
        except Exception as e:
            except_as.append(e)  # 记录没有信息的AS列表
        if item_as_country not in direct_country_as_dict.keys():
            direct_country_as_dict[item_as_country] = direct_as2prefix_dict[item_as]
        else:
            direct_country_as_dict[item_as_country].extend(direct_as2prefix_dict[item_as])
    print("国家key数量:", len(direct_country_as_dict.keys()))
    print("Except AS 记录数量：", len(except_as))
    # print(direct_as2prefix_dict["141771"])
    direct_country_ip_num = []  # 存储直联国家前缀及IP规模
    ipv4_prefix_sum_all = 0
    ipv4_num_all = 0
    for country_item in direct_country_as_dict.keys():
        if country_item == "CN":
            continue
        ipv4_prefix_sum = 0
        ipv4_num = 0
        for prefix_item in direct_country_as_dict[country_item]:
            ipv4_prefix_sum += 1
            ipv4_num += len(IP(prefix_item))
        ipv4_prefix_sum_all += ipv4_prefix_sum
        ipv4_num_all += ipv4_num
        direct_country_ip_num.append([country_item, country2name[country_item], ipv4_prefix_sum, ipv4_num])
    direct_country_ip_num.sort(reverse=True, key=lambda elem: elem[3])
    """
    参考Tele的数据，CN2002年国际互联带宽为47398G,其中HK为33829G
    
    """
    cap_direct_cn = []  # 存储CN分方向的带宽
    for item in direct_country_ip_num:
        temp_item = []
        temp_item.extend(item)
        temp_item.append(item[-1]/ipv4_num_all)
        temp_item.append((item[-1]/ipv4_num_all) * (47398-33829))
        print(temp_item)
        cap_direct_cn.append(temp_item)
    save_cap_path = "../000LocalData/global_traffic_model/cap_cn.csv"
    write_to_csv(cap_direct_cn, save_cap_path)
    print("- - - - -5)网络仿真实验- - - ")
    print("即国际网络仿真模型")
    print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")


def rib_analysis():
    """
    处理rib文件

    :return :
    """
    as2country, as2info = gain_as2country()
    print("asWhois信息记录：", len(as2country))
    country2continent, country2name = gain_country2info()
    print("countryWhois信息记录：", len(country2continent))
    rib_dict = {}
    """
    1）判断协议类型，包括TABLE_DUMP2和TABLE_DUMP2_AP
    2）按照来源构建各自的RIB，中国电信(AS4134)、中国联通(4837)、中国移动（9808）、HangZhouIX（AS139136）
    3）数据格式按照来源ASN作为key，[[ip_prefix, as_path], ...]作为value
    """
    file_read = open(rib_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("|")
        # print(line)
        if line[0] == "TABLE_DUMP2":
            if line[4] not in rib_dict.keys():
                rib_dict[line[4]] = [[line[5], line[6]]]
            else:
                rib_dict[line[4]].append([line[5], line[6]])
        elif line[0] == "TABLE_DUMP2_AP":
            if line[4] not in rib_dict.keys():
                rib_dict[line[4]] = [[line[5], line[6], line[7]]]
            else:
                rib_dict[line[4]].append([line[5], line[6], line[7]])
        else:
            print("ERROR!")
    print("RIB来源记录:", rib_dict.keys())
    all_line = 0
    for rib_key in rib_dict.keys():
        print("AS"+rib_key+":", len(rib_dict[rib_key]))
        all_line = all_line + len(rib_dict[rib_key])
        """
        将分来源的RIB各自存储
        """
        rib_re_file = "../000LocalData/global_traffic_model/as"+rib_key+"_rib.csv"
        write_to_csv(rib_dict[rib_key], rib_re_file)

    print("RIB各来源条目总记录:", all_line)
    """
    针对每个RIB开展研究，以电信4134为例    
    """
    rib_analysis_table_dump2("4134", rib_dict["4134"])
    # rib_analysis_table_dump2("4837", rib_dict["4837"])
    # rib_analysis_table_dump2("9808", rib_dict["9808"])


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    rib_analysis()
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
