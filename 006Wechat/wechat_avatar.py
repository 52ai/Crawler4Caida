# coding:utf-8
"""
create on June 25,2019 by Wayne Yu
Function: 生成微信好友头像图片墙
"""
from wxpy import *
import math
from PIL import Image
import os


# 创建头像存放文件夹
def create_filepath():
    # avatar_dir = os.getcwd() + "\\wechat\\"
    # if not os.path.exists(avatar_dir):
    #     os.mkdir(avatar_dir)
    avatar_dir = "../000LocalData/wechat/"
    return  avatar_dir


# 保存好友头像
def save_avatar(avatar_dir):
    bot = Bot()  # 初始化机器人，扫码登陆
    friends = bot.friends(update=True)
    num = 0
    for friend in friends:
        friend.get_avatar(avatar_dir + '\\' + str(num) + ".png")
        print('好友昵称：%s' % friend.nick_name)
        num = num + 1


# 拼接头像
def joint_avatar(path):
    length = len(os.listdir(path))  # 获取文件夹头像的个数
    image_size = 3000  # 设置画布大小
    each_size = math.ceil( image_size / math.floor(math.sqrt(length)))  # 设置每个头像的大小
    x_lines = math.ceil(math.sqrt(length))
    y_lines = math.ceil(math.sqrt(length))
    image = Image.new('RGB', (each_size * x_lines, each_size * y_lines))
    x = 0
    y = 0
    cnt = 0
    for (root, dirs, files) in os.walk(path):
        # print(files)
        for pic_name in files:
            try:
                with Image.open(path + pic_name) as img:
                    img = img.resize((each_size, each_size))
                    image.paste(img, (x * each_size, y * each_size))
                    x += 1
                    cnt += 1
                    if x == x_lines:
                        x = 0
                        y += 1
            except IOError:
                print("头像读取失败")
                print(x, y, cnt, pic_name)
    image = image.save(os.getcwd() + "/wechat.png")
    print("Done!")


if __name__ == "__main__":
    avatar_dir = create_filepath()
    save_avatar(avatar_dir)
    joint_avatar(avatar_dir)
