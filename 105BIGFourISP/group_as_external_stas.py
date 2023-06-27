# coding:utf-8
"""
create on Jun 27, 2023 By Wayne YU

Function:

按照电信、移动、联通、广电四个Group组分别统计其连通度（去重），组内互联不计算在内，且需输出详细的对端AS网络

"""
import time
import csv


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
        as2org_dic[as_number] = as_org.split(",")[0]
    return as2org_dic


def group_as_external_stas():
    """
    统计，big four ISP 的外部连通度（去重）
    :return:
    """
    as_2_country = gain_as2country_caida()
    as_2_org = gain_as2org_caida()
    big_four_as = {"ct": ['4134', '4809', '23764'],
                   "cm": ['9808', '58453'],
                   "cu": ['4837', '9929', '10099'],
                   "cb": ['146788', '58852', '63704', '131488', '63590',
                          '131506', '131565', '59084', '23771', '45078',
                          '59016', '59064', '63581', '24150', '24139',
                          '55977', '63607', '58834', '7576', '55961',
                          '63701', '63540', '131526', '146802', '17969',
                          '24423', '63719', '131132', '23850', '9812',
                          '23841', '59026', '63539', '17429', '131562',
                          '45106', '17962']}

    big_four_external_as = {"ct": [],
                            "cm": [],
                            "cu": [],
                            "cb": []}
    file_in = "../000LocalData/as_relationships/serial-1/20230601.as-rel.txt"
    with open(file_in, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if line.strip().find("#") == 0:
                continue
            line = line.strip().split("|")
            left_as = line[0]
            right_as = line[1]
            # print(left_as, right_as)

            for key in big_four_as:
                if left_as in big_four_as[key] and right_as not in big_four_as[key]:
                    big_four_external_as[key].append(right_as)

                if right_as in big_four_as[key] and left_as not in big_four_as[key]:
                    big_four_external_as[key].append(left_as)

    print("中国电信外部连通度, %s(去重前)，%s(去重后)" % (len(big_four_external_as["ct"]), len(set(big_four_external_as["ct"]))))
    print("中国移动外部连通度, %s(去重前)，%s(去重后)" % (len(big_four_external_as["cm"]), len(set(big_four_external_as["cm"]))))
    print("中国联通外部连通度, %s(去重前)，%s(去重后)" % (len(big_four_external_as["cu"]), len(set(big_four_external_as["cu"]))))
    print("中国广电外部连通度, %s(去重前)，%s(去重后)" % (len(big_four_external_as["cb"]), len(set(big_four_external_as["cb"]))))
    print("中国广电外部连接AS详细信息(ASN/机构/国家):")
    for item in list(set(big_four_external_as["cb"])):
        print(item, "/", as_2_org[item], "/", as_2_country[item])


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    group_as_external_stas()
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
