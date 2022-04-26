# coding:utf-8
"""
create on Mar 11, 2022 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

依托CAIDA解决asn_info信息更新不及时的问题

"""

import jsonlines
import time
import csv


def write_to_csv(res_list, des_path, title_list):
    """
    把给定的List，写到指定路径文件中
    :param res_list:
    :param des_path:
    :param title_list:
    :return None:
    """
    print("write file <%s>.." % des_path)
    csv_file = open(des_path, "w", newline='', encoding='utf-8')
    try:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"')
        writer.writerow(title_list)
        for i in res_list:
            writer.writerow(i)
    except Exception as e_csv:
        print(e_csv)
    finally:
        csv_file.close()
    print("write finish!")


def gain_asn_info():
    """
    根据asns.jsonl获取需要的asn信息
    :return:
    """
    asns_file = "../000LocalData/as_rank_caida/asns.jsonl"
    asn_info_result = []  # 存储asn基础信息
    with jsonlines.open(asns_file) as file_read:
        for obj in file_read:
            asn = obj["asn"]
            asn_name = obj["asnName"]
            asn_org = "NONE"
            try:
                asn_org = obj["organization"]["orgName"]
            except Exception as e:
                print(e)
            asn_country = obj["country"]["iso"]

            print(asn, asn_name, asn_org, asn_country)
            asn_info_result.append([asn, asn_name, asn_org, asn_country])
    asn_info_result.sort(reverse=False, key=lambda elem: int(elem[0]))
    save_file = "../000LocalData/as_Gao/asn_info_from_caida.csv"
    title_line = ["asn", "asn_name", "asn_org", "asn_country"]
    write_to_csv(asn_info_result, save_file, title_line)


if __name__ == "__main__":
    time_start = time.time()  # 记录程序启动的时间
    gain_asn_info()
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start))
