# coding:utf-8
"""
create on Apr 14, 2020 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

读取已从Github下载的新冠疫情数据，根据绘图需求进行处理并输出

"""

import json
import datetime
import csv


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return None:
    """
    print("write file <%s> ..." % des_path)
    csvFile = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csvFile, delimiter=",")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csvFile.close()
    print("write finish!")


if __name__ == "__main__":

    date_str = str(datetime.datetime.now().strftime('%Y%m%d'))
    file_in_str = "../000LocalData/Covid2019/Covid2019_data" + date_str + ".json"
    file_in = open(file_in_str, encoding='utf-8')
    json_data = json.load(file_in)

    # print(json_data)

    # 数据存储

    data_source_global = []  # 全球疫情源数据列表
    data_source_cn = []  # 中国疫情源数据列表
    province_short_name_list = []  # 省份列表
    confirmed_count_list = []  # 确诊人数列表
    cured_count = []  # 治愈人数列表
    dead_count_list = []  # 死亡人数列表

    # 添加表头描述项
    temp_list_global = []
    # temp_list_global.append("国家名称")  # 国家名称
    # temp_list_global.append("国家英文名称")  # 国家英文名称
    # temp_list_global.append("累计确诊")  # 累计确诊
    # temp_list_global.append("现有确诊")  # 现有确诊
    # temp_list_global.append("累计治愈")  # 累计治愈
    # temp_list_global.append("累计死亡")  # 累计死亡
    # data_source_global.append(temp_list_global)
    # temp_list_global = []

    # 添加表头描述项
    temp_list_cn = []
    # temp_list_cn.append("省份名称")  # 省份名称
    # temp_list_cn.append("累计确诊")  # 累计确诊
    # temp_list_cn.append("现有确诊")  # 现有确诊
    # temp_list_cn.append("累计治愈")  # 累计治愈
    # temp_list_cn.append("累计死亡")  # 累计死亡
    # data_source_cn.append(temp_list_cn)
    # temp_list_cn = []

    for k in range(len(json_data['results'])):
        # print(json_data['results'][k]['countryName'], json_data['results'][k]['countryEnglishName'],
        #       json_data['results'][k]['currentConfirmedCount'])

        if json_data['results'][k]['countryName'] == json_data['results'][k]['provinceShortName']:
            # print(json_data['results'][k]['countryName'], json_data['results'][k]['provinceShortName'])
            # temp_list_global.append(json_data['results'][k]['countryName'])  # 国家名称
            if json_data['results'][k]['countryEnglishName'] is None:
                continue
            temp_list_global.append(json_data['results'][k]['countryEnglishName'])  # 国家英文名称
            temp_list_global.append((json_data['results'][k]['confirmedCount']))  # 累计确诊
            # temp_list_global.append(json_data['results'][k]['currentConfirmedCount'])  # 现有确诊
            # temp_list_global.append(json_data['results'][k]['curedCount'])  # 累计治愈
            # temp_list_global.append(json_data['results'][k]['deadCount'])  # 累计死亡
            data_source_global.append(temp_list_global)
            temp_list_global = []

        if json_data['results'][k]['countryName'] == '中国':
            province_short_name = json_data['results'][k]['provinceShortName']
            if "待明确地区" == province_short_name:
                continue
            confirmed_count = json_data['results'][k]['confirmedCount']

            temp_list_cn.append(province_short_name)  # 省份简称
            temp_list_cn.append(confirmed_count)  # 累计确诊
            # temp_list_cn.append(json_data['results'][k]['currentConfirmedCount'])  # 现有确诊
            # temp_list_cn.append(json_data['results'][k]['curedCount'])  # 累计治愈
            # temp_list_cn.append(json_data['results'][k]['deadCount'])  # 累计死亡

            data_source_cn.append(temp_list_cn)
            temp_list_cn = []

    print("已获取的全球数据（包括重要邮轮疫情）：", len(data_source_global))
    data_source_global.sort(reverse=True, key=lambda elem: int(elem[1]))  # 按照累计确诊人数降序
    print(data_source_global)
    save_path = "../000LocalData/Covid2019/Covid_2019_global" + date_str + ".csv"
    write_to_csv(data_source_global, save_path)

    print("已获取的地方数据（包括中国总数）34+1：", len(data_source_cn))
    data_source_cn.sort(reverse=True, key=lambda elem: int(elem[1]))  # 按照累计确诊人数降序
    print(data_source_cn)
    save_path = "../000LocalData/Covid2019/Covid_2019_cn" + date_str + ".csv"
    write_to_csv(data_source_cn, save_path)
