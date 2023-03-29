# coding:utf-8
"""
create on Feb 22, 2023 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

以RIB数据作为输入，研究每个Tier1 ISP的路由通告量，路由条目、IP地址量。
并以此为契机，开展Tier1 ISP网间和网内拓扑的构建研究

"""
import time
import csv
from IPy import IP

rib_file = "../000LocalData/BGPData/rib_live/rib_2023-01-13_181.txt"
as_info_file = '../000LocalData/as_Gao/asn_info_from_caida.csv'
country_info_file = '../000LocalData/as_geo/GeoLite2-Country-Locations-zh-CN.csv'


def write_to_csv(res_list, des_path, title_line):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :param title_line:
    :return None:
    """
    print("write file <%s> ..." % des_path)
    csv_file = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csv_file)
        writer.writerow(title_line)
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
    print("write finish!")


def gain_as2info_caida():
    """
    根据Caida asn info获取as对应的信息，as_name、as_org、as_country
    :return as2info_result:
    """
    as2info_result = {}  # 存储as号到info的映射关系
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split(",")
        # print(line)
        as_number = line[0]
        as_name = line[1]
        as_org = line[2].strip("\"")
        as_country = line[-1]
        as2info_result[as_number] = [as_name, as_org, as_country]
    return as2info_result


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
    根据传入的asn及其RIB List，开展相关分析
    :param asn:
    :param rib_list:
    :return:
    """
    as2info = gain_as2info_caida()
    country2continent, country2name = gain_country2info()
    print("===========TABLE_DUMP2 RIB 详细分析==============")
    print("RIB来源：AS" + asn)
    print("RIB总的记录数:", len(rib_list))
    """
    针对每个RIB可以做很详细的分析：
    1）现网活跃AS网络，按国家、大洲维度进行统计分析。
    2）现网通告路由前缀以及IPv4地址数量，按AS网络、国家、大洲维度进行统计分析。
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
            item_as_country = as2info[item_as][-1]
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
            item_as_country = as2info[item_as][-1]
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
    global_prefix = 0
    global_ipv4_num = 0
    global_ipv4_num_list = []  # 存储去重的ipv4地址
    for as_key in as2prefix_dict.keys():
        for prefix_item in as2prefix_dict[as_key]:
            global_prefix += 1
            global_ipv4_num += len(IP(prefix_item))

    print("全球 IPv4前缀规模:%s, IPv4地址数量:%s, IPv4地址数量（去重）:%s" % (global_prefix, global_ipv4_num, len(global_ipv4_num_list)))
    """
    统计Tier1的路由通告前缀数量、网内IP地址数量
    """
    tier1_list = ["3356", "1299", "2914", "6762", "3257",
                  "6453", "6461", "3491", "5511", "12956",
                  "701", "1239", "7018", "3320", "6830",
                  "174", "6939", "4134"]
    tier1_ip_list = []
    for item_as in tier1_list:
        item_as_ipv4_num = 0
        for ipv4_prefix in as2prefix_dict[item_as]:
            item_as_ipv4_num += len(IP(ipv4_prefix))
        print("AS%s, %s, %s, IPv4前缀规模:%s, IPv4地址数量：%s"
              % ("AS"+item_as, as2info[item_as][1], as2info[item_as][-1], len(as2prefix_dict[item_as]), item_as_ipv4_num))
        tier1_ip_list.append(["AS"+item_as,
                              as2info[item_as][0],
                              as2info[item_as][1],
                              as2info[item_as][2],
                              len(as2prefix_dict[item_as]),
                              item_as_ipv4_num])
    save_path = "../000LocalData/tier1/tier1_ip_result.csv"
    title_str = ["ASN", "AS NAME", "AS ORG", "AS COUNTRY", "ip prefix", "ip num"]
    write_to_csv(tier1_ip_list, save_path, title_str)

    global_as_ip_list = []
    for item_as in as2prefix_dict.keys():
        item_as_ipv4_num = 0
        for ipv4_prefix in as2prefix_dict[item_as]:
            item_as_ipv4_num += len(IP(ipv4_prefix))
        as_country = "ZZ"
        try:
            as_country = as2info[item_as][2]
        except Exception as e:
            except_as.append(e)
        # print("AS%s, IPv4前缀规模:%s, IPv4地址数量：%s" % ("AS"+item_as, len(as2prefix_dict[item_as]), item_as_ipv4_num))
        global_as_ip_list.append(["AS"+item_as,
                                  as_country,
                                  len(as2prefix_dict[item_as]),
                                  item_as_ipv4_num])
    save_path = "../000LocalData/tier1/global_as_ip_result.csv"
    title_str = ["ASN", "AS COUNTRY", "ip prefix", "ip num"]
    write_to_csv(global_as_ip_list, save_path, title_str)


def rib_analysis():
    """
    处理181 rib文件，分析电信（AS4134）的路由表，形成网络互联、网络路由等分析模板
    :return:
    """
    as2info = gain_as2info_caida()
    print("asWhois信息记录:", len(as2info))
    country2continent, country2name = gain_country2info()
    print("countryWhois信息记录：", len(country2continent))
    """
    1)判断协议类型，包括TABLE_DUMP2和TABLE_DUMP2_AP
    2)按照来源构建各自的RIB：AS4134、AS4837、AS9808
    3)数据格式按照来源ASN作为key, [[ip_prefix, as_path], ...]作为value   
    """
    rib_dict = {}
    with open(rib_file, 'r', encoding='utf-8') as f:
        for line in f.readlines():
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
