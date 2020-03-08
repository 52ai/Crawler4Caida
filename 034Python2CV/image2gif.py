# coding:utf-8
"""
create on Mar 8, 2020 By Wenyan YU Using Python 3.7
Email: ieeflsyu@outlook.com

Function:
实现读取多张图片，存储为gif

"""

import imageio
import os


root_dir = u'C://Users//Wayne//Desktop//录屏//image'
file_names = sorted((fn for fn in os.listdir(root_dir) if fn.endswith('.PNG')))
file_names.reverse()
images = []
for file_name in file_names:
    print(file_name)
    images.append(imageio.imread(root_dir + "//" + file_name))
print(len(images))
save_path = root_dir + "//out.gif"
imageio.mimsave(save_path, images, 'GIF', duration=1)

