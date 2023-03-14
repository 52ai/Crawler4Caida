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
# from IPy import IP

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


def rib_analysis():
    """
    处理181 rib文件，分析电信（AS4134）的路由表，形成网络互联、网络路由等分析模板
    :return:
    """
    as2info = gain_as2info_caida()
    print("asWhois信息记录:", len(as2info))
    country2continent, country2name = gain_country2info()
    print("countryWhois信息记录：", len(country2continent))
    # rib_dict = {}
    """
    1)判断协议类型，包括TABLE_DUMP2和TABLE_DUMP2_AP
    2)按照来源构建各自的RIB：AS4134、AS4837、AS9808
    3)数据格式按照来源ASN作为key, [[ip_prefix, as_path], ...]作为value   
    """
    with open(rib_file, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip().split("|")
            print(line)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    rib_analysis()
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
