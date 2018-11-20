# coding:utf-8
"""
create on Nov 20, 2018 by Wayne
Fun:实现自动下载跟谁学平台视频数据

eg:
词悬浮公开课第一节视频连接为
https://dal-video.wenzaizhibo.com/a97f492f895460ce15a2f315c543361d/5bf4009b/00-x-upload/video/101930188_2d96294ae0fe8a12811957e1eb9430de_Wv9Xdfro.mp4
20181120 15:15
先把词悬浮的5节公开课下完，后面再对程序进行优化，比如通过分析页面自动获取下载链接、加下载进度条、实现多线程下载以便增加下载速度。
对于词悬浮188节课全集，已经放弃买了，性价比不高，两种获取途径：
第一种、直接通过网站进行破解（有空可以研究下，就当学习学习技术）
第二种、在闲鱼上买百度云的资源（在第一种无法获取的情况下，可以通过这种方法获取）
"""
import requests


def download_file(file_url, file_name):
    r = requests.get(file_url, stream=True)
    with open(file_name, "wb") as mp4:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                mp4.write(chunk)


if __name__ == "__main__":
    url_list = [["https://dal-video.wenzaizhibo.com/a97f492f895460ce15a2f315c543361d/5bf4009b/00-x-upload/video/101930188_2d96294ae0fe8a12811957e1eb9430de_Wv9Xdfro.mp4", "词悬浮之词汇速记训练营1.mp4"],
                ["https://dws-video.wenzaizhibo.com/bcc461c93eea3e298ed3d920d072f5ef/5bf40786/00-x-upload/video/101939191_2ef5f1c378626d79f28861572c300c01_BPnEoBhu.mp4", "词悬浮之词汇速记训练营2.mp4"],
                ["https://dws-video.wenzaizhibo.com/8133557bfd1c082824ea63c090bbc1ac/5bf407c3/00-x-upload/video/101951123_ad4585e4f06ed41124d6a19b98d2252c_XoeFnx0S.mp4", "词悬浮之词汇速记训练营3.mp4"],
                ["https://dws-video.wenzaizhibo.com/d36713d3ce47e166f17cfc06d29bfac4/5bf407f1/00-x-upload/video/101960083_dbef7450246b3cedfb99df71a87d8e26_B9vzr93I.mp4", "词悬浮之词汇速记训练营4.mp4"],
                ["https://dws-video.wenzaizhibo.com/084763e24f33d61f0cddbe6db3a59548/5bf4081e/00-x-upload/video/101961394_edf2facfb2724c2c55795f677647fd39_lRrK4eVJ.mp4", "词悬浮之词汇速记训练营5.mp4"]]
    print("start")
    for item in url_list:
        download_file(item[0], item[1])
        print(item[1], " 下载完成")
    print("end")
