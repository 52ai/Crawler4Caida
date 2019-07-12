"""
    作者：钟平声
    功能：删除符合条件的记录
    日期：2019.7.11
    版本：5.0
    功能5.0：增加日期处理
"""
# coding: utf-8
import pandas as pd
from datetime import datetime

def delete_specific_rows(filename,provence_list,carrier_list,delete_days):

    # 读 excel 文件，指定“测试时间”为时间读取格式
    # data = pd.read_excel(filename, index_col=None, parse_dates=['测试时间'])
    data = pd.read_excel(filename, index_col=None, parse_dates=["测试时间"])
    print(data)
    excel_data = pd.DataFrame(data)
    print(excel_data)
    list_index = 0
    for i in range(0,6):

        #删除符合条件的源点
        del_dates = delete_days
        print(excel_data['目的运营商'])
        excel_data = excel_data.drop(excel_data[(excel_data['源省份'] == provence_list[list_index])\
                                                & (excel_data['源运营商'] == carrier_list[list_index])].index)
        #删除符合条件的目的点
        # excel_data = excel_data.drop(excel_data[(excel_data['目的省份'] == provence_list[list_index]) \
        #                                         & (excel_data['目的运营商'] == carrier_list[list_index])].index)
        #                                         & (excel_data['测试时间'].isin(del_dates)].index)
        #print(excel_data['目的省份'])
        list_index += 1

    # 更新文件
    excel_data.to_excel(filename,index=None,header=None)

def main():

    #print("请输入需要处理的excel文档：")
    filename = "./test.xlsx"

    print("处理文件名：", filename)
    provence_list = ['四川','山西','江苏','江苏','江苏','甘肃','青海']
    carrier_list = ['电信','电信','电信','移动','联通','电信','电信']

    delete_days = pd.date_range('2019-7-1','2019-7-10')
    print(delete_days)
    delete_specific_rows(filename,provence_list,carrier_list,delete_days)

if __name__ == "__main__":
    main()


