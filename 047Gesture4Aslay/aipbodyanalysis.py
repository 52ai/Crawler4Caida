# coding:utf-8
"""
create on July 16, 2020 By Wenyan YU
Email: ieeflsyu@outlook.com

function:

尝试着使用云端资源，来解决本地计算不足的问题，那就从百度云API开始吧
后面有空还可以研究亚马逊云、谷歌云、阿里云、腾讯云等云服务

"""
from aip import AipBodyAnalysis
import time
import base64


def gain_access_info():
    """
    读取文件获取key信息
    :return:
    """
    access_file = "../000LocalData/BaiduCloud/gr4aslay_access.txt"
    file_read = open(access_file, 'r', encoding='utf-8')
    app_id, api_key, secret_key = "", "", ""
    for line in file_read.readlines():
        line = line.split("|")
        app_id = line[0]
        api_key = line[1]
        secret_key = line[2]
    return app_id, api_key, secret_key


def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()


def save_base64_png(image_data, file_path):
    """
    根据PNG base64数据，存储为指定地址的PNG图片
    :param image_data:
    :param file_path:
    :return:
    """
    image_data = base64.b64decode(image_data)
    with open(file_path, 'wb') as f:
        f.write(image_data)
    print("write base64 PNG file successful:", file_path)


def gesture_recognition(client):
    """
    探索手势识别功能
    :return:
    """
    print(client)
    test_image = "../000LocalData/BaiduCloud/GestureRecognition/seven.png"
    image = get_file_content(test_image)
    result = client.gesture(image)
    print(result['result'][0]['classname'])


def body_segment(client):
    """
    探索人像分割功能
    :param client:
    :return:
    """
    print(client)
    test_image = "../000LocalData/BaiduCloud/HumanSegmentation/human002.jpg"
    image = get_file_content(test_image)
    my_options = dict()
    my_options["type"] = "foreground"
    result = client.bodySeg(image, my_options)
    result_save_path = "../000LocalData/BaiduCloud/HumanSegmentation/result_foreground.png"
    save_base64_png(result['foreground'], result_save_path)
    print(result)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    my_app_id, my_api_key, my_secret_key = gain_access_info()
    my_client = AipBodyAnalysis(my_app_id, my_api_key, my_secret_key)
    # gesture_recognition(my_client)
    body_segment(my_client)
    time_end = time.time()  # 记录结束的时间
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start))
