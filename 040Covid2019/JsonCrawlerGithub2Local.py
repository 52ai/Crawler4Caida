# coding:utf-8
"""
create on Apr 14, 2020 By Wayne YU
Function：

将Github上的新冠疫情源数据下载到本地

url = 'https://github.com/BlankerL/DXY-2019-nCoV-Data/blob/master/json/DXYArea.json'
url = 'https://raw.githubusercontent.com/BlankerL/DXY-2019-nCoV-Data/master/json/DXYArea.json'

"""
import datetime
import json
import requests


# 获取所有数据json文件
def download_json(url):
    """

    :param url:
    :return:
    """
    print("downloading json file %s" % (url))
    response = requests.get(url)
    version_info = response.text
    version_info_python = json.loads(version_info)

    print(version_info)
    path = '../000LocalData/Covid2019/Covid2019_data' + str(datetime.datetime.now().strftime('%Y%m%d')) + '.json'
    # 将json格式化的数据保存
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(json.dumps(version_info_python, indent=4))


if __name__ == "__main__":
    url = 'https://raw.githubusercontent.com/BlankerL/DXY-2019-nCoV-Data/master/json/DXYArea.json'
    download_json(url)
