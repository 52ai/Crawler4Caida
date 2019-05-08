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
第一种、直接通过网站进行破解（有空可以研究下，就当学习学习技术，注意不要传播，怕有法律风险）
第二种、在闲鱼上买百度云的资源（在第一种无法获取的情况下，可以通过这种方法获取）

url_list = [["https://dal-video.wenzaizhibo.com/a97f492f895460ce15a2f315c543361d/5bf4009b/00-x-upload/video/101930188_2d96294ae0fe8a12811957e1eb9430de_Wv9Xdfro.mp4", "词悬浮之词汇速记训练营1.mp4"],
            ["https://dws-video.wenzaizhibo.com/bcc461c93eea3e298ed3d920d072f5ef/5bf40786/00-x-upload/video/101939191_2ef5f1c378626d79f28861572c300c01_BPnEoBhu.mp4", "词悬浮之词汇速记训练营2.mp4"],
            ["https://dws-video.wenzaizhibo.com/8133557bfd1c082824ea63c090bbc1ac/5bf407c3/00-x-upload/video/101951123_ad4585e4f06ed41124d6a19b98d2252c_XoeFnx0S.mp4", "词悬浮之词汇速记训练营3.mp4"],
            ["https://dws-video.wenzaizhibo.com/d36713d3ce47e166f17cfc06d29bfac4/5bf407f1/00-x-upload/video/101960083_dbef7450246b3cedfb99df71a87d8e26_B9vzr93I.mp4", "词悬浮之词汇速记训练营4.mp4"],
            ["https://dws-video.wenzaizhibo.com/084763e24f33d61f0cddbe6db3a59548/5bf4081e/00-x-upload/video/101961394_edf2facfb2724c2c55795f677647fd39_lRrK4eVJ.mp4", "词悬浮之词汇速记训练营5.mp4"]]

url_list = [["https://dws-video.wenzaizhibo.com/eacbd018618984e7ea6ede4dbe9ae298/5bf6dd4b/00-x-upload/video/101930946_dccf86aaeac9b4a5d22f7f6f73606799_ACO7dxeK.mp4", "治愈系英语语法（结构的力量）1.mp4"],
            ["https://dws-video.wenzaizhibo.com/a3ea9d3c176ca4813205885c48707757/5bf6ddc9/00-x-upload/video/101941345_bf796bd3ddb3ec2df1c935783cba6a6c_RPMZNQNW.mp4", "治愈系英语语法（结构的力量）2.mp4"],
            ["https://dws-video.wenzaizhibo.com/b3fa1e3d5614efa26d1b54887a994835/5bf6ddeb/00-x-upload/video/101951513_8ded814022dff9793681e4dc333821f7_AVibSsBj.mp4", "治愈系英语语法（结构的力量）3.mp4"],
            ["https://dws-video.wenzaizhibo.com/f9f6a72f895ec70c44bfb3055c363f5d/5bf6de0b/00-x-upload/video/101960420_e9fcc1deba2d5b998876ce1e530a938f_FeWYrY5Q.mp4", "治愈系英语语法（结构的力量）4.mp4"],
            ["https://dal-video.wenzaizhibo.com/c465b5c4464dd4184c842f841823c18e/5bf6dc73/00-x-upload/video/101961959_46ff2903e8329fb5fa792ecbe18ea8ad_TAYPOMJx.mp4", "治愈系英语语法（结构的力量）5.mp4"]]

url_list = [["https://dws-video.wenzaizhibo.com/f9ce79a273f44e14de61aff74c101146/5bf6defe/00-x-upload/video/101938187_321f608db6f3e44b24ac51ae6f13f0db_kxn8Pd7A.mp4", "纯正英语口语（让你马上开口说英语）1.mp4"],
            ["https://dws-video.wenzaizhibo.com/fab34786450ce56ed3410a937ca4ae2e/5bf6df63/00-x-upload/video/101949616_03a2bfea33715d3fd8bcfc44a54d4c3b_co0YCgSW.mp4", "纯正英语口语（让你马上开口说英语）2.mp4"],
            ["https://dws-video.wenzaizhibo.com/30b85805f76e5dae117f233d0fca496d/5bf6df8a/00-x-upload/video/101959533_343c99ad33b754f316487580a7fada53_lhKHSS3X.mp4", "纯正英语口语（让你马上开口说英语）3.mp4"],
            ["https://dws-video.wenzaizhibo.com/d8ce3cab6a668893dadab4a1165a642d/5bf6dfac/00-x-upload/video/101964240_b559e498942159bbf6b07760c69a7811_luDFSVdZ.mp4", "纯正英语口语（让你马上开口说英语）4.mp4"],
            ["https://dws-video.wenzaizhibo.com/e9152545296c27be63aba64fb1c93541/5bf6dfe9/00-x-upload/video/101746940_70bed963e35885fabc5bfa32861fa76c_Xy9QPLUb.mp4", "零基础直达流利口语1.mp4"],
            ["https://dws-video.wenzaizhibo.com/7c4735686dd9e0b50a89c1c1abcc24aa/5bf6e06c/00-x-upload/video/101753764_f22fa90dfe1aa19205123186ac4f0f0e_sJ5DMAtf.mp4", "零基础直达流利口语2.mp4"],
            ["https://dws-video.wenzaizhibo.com/6fccd806deb308274d6dd34c46426138/5bf6e0ce/00-x-upload/video/101759860_ad3dc947fa135e58b1828abbf385e068_5q4g1mfC.mp4", "零基础直达流利口语3.mp4"],
            ["https://dws-video.wenzaizhibo.com/9a4a0e3c2bfa0490578c64f288145303/5bf6e0e3/00-x-upload/video/101765082_60122d2374dc2eed1ac9c23107ea83a1_QnXjh2s4.mp4", "零基础直达流利口语4.mp4"],
            ["https://dws-video.wenzaizhibo.com/357e1f50baaa5a2cea7c470f8dd41428/5bf6e0f8/00-x-upload/video/101768173_0511f25c3bf1e46e8ddae7d2792f80db_OUh1rWo0.mp4", "零基础直达流利口语5.mp4"],
            ["https://dws-video.wenzaizhibo.com/530e7272a69eb7999fccd57adf38117e/5bf6e5bb/00-x-upload/video/101938396_f844531ec947762cc9c66ac9e2439b9b_fzOGGkze.mp4", "5天魔法英语特训营1.mp4"],
            ["https://dws-video.wenzaizhibo.com/b79ed7cf4b296366d851c87c1d95496d/5bf6e5e3/00-x-upload/video/101950236_77cb6f17a124f66751ab6878740c5305_yMdJjKIX.mp4", "5天魔法英语特训营2.mp4"],
            ["https://dws-video.wenzaizhibo.com/5ec9ff7bf5c9c04c431029bbe612a879/5bf6e5fe/00-x-upload/video/101959664_922a548016bf6d6bc87dcb3b1ebfdbdc_KA7iHZ5u.mp4", "5天魔法英语特训营3.mp4"],
            ["https://dws-video.wenzaizhibo.com/484c98921f9b93af3e0c6cec973091a0/5bf6e617/00-x-upload/video/101964932_7d43e8e08e682935005c907429c40d93_Q9aRyDY6.mp4", "5天魔法英语特训营4.mp4"]]
"""
import requests
import threading


url_list = [["https://dws-video.wenzaizhibo.com/9479218336fb9535c396d51aff7c3451/5bf83046/00-x-upload/video/101938187_321f608db6f3e44b24ac51ae6f13f0db_kxn8Pd7A.mp4", "纯正英语口语（让你马上开口说英语）1.mp4"],
            ["https://dws-video.wenzaizhibo.com/fab34786450ce56ed3410a937ca4ae2e/5bf6df63/00-x-upload/video/101949616_03a2bfea33715d3fd8bcfc44a54d4c3b_co0YCgSW.mp4", "纯正英语口语（让你马上开口说英语）2.mp4"],
            ["https://dws-video.wenzaizhibo.com/30b85805f76e5dae117f233d0fca496d/5bf6df8a/00-x-upload/video/101959533_343c99ad33b754f316487580a7fada53_lhKHSS3X.mp4", "纯正英语口语（让你马上开口说英语）3.mp4"],
            ["https://dws-video.wenzaizhibo.com/d8ce3cab6a668893dadab4a1165a642d/5bf6dfac/00-x-upload/video/101964240_b559e498942159bbf6b07760c69a7811_luDFSVdZ.mp4", "纯正英语口语（让你马上开口说英语）4.mp4"],
            ["https://dws-video.wenzaizhibo.com/e9152545296c27be63aba64fb1c93541/5bf6dfe9/00-x-upload/video/101746940_70bed963e35885fabc5bfa32861fa76c_Xy9QPLUb.mp4", "零基础直达流利口语1.mp4"],
            ["https://dws-video.wenzaizhibo.com/7c4735686dd9e0b50a89c1c1abcc24aa/5bf6e06c/00-x-upload/video/101753764_f22fa90dfe1aa19205123186ac4f0f0e_sJ5DMAtf.mp4", "零基础直达流利口语2.mp4"],
            ["https://dws-video.wenzaizhibo.com/6fccd806deb308274d6dd34c46426138/5bf6e0ce/00-x-upload/video/101759860_ad3dc947fa135e58b1828abbf385e068_5q4g1mfC.mp4", "零基础直达流利口语3.mp4"],
            ["https://dws-video.wenzaizhibo.com/9a4a0e3c2bfa0490578c64f288145303/5bf6e0e3/00-x-upload/video/101765082_60122d2374dc2eed1ac9c23107ea83a1_QnXjh2s4.mp4", "零基础直达流利口语4.mp4"],
            ["https://dws-video.wenzaizhibo.com/357e1f50baaa5a2cea7c470f8dd41428/5bf6e0f8/00-x-upload/video/101768173_0511f25c3bf1e46e8ddae7d2792f80db_OUh1rWo0.mp4", "零基础直达流利口语5.mp4"],
            ["https://dws-video.wenzaizhibo.com/530e7272a69eb7999fccd57adf38117e/5bf6e5bb/00-x-upload/video/101938396_f844531ec947762cc9c66ac9e2439b9b_fzOGGkze.mp4", "5天魔法英语特训营1.mp4"],
            ["https://dws-video.wenzaizhibo.com/b79ed7cf4b296366d851c87c1d95496d/5bf6e5e3/00-x-upload/video/101950236_77cb6f17a124f66751ab6878740c5305_yMdJjKIX.mp4", "5天魔法英语特训营2.mp4"],
            ["https://dws-video.wenzaizhibo.com/5ec9ff7bf5c9c04c431029bbe612a879/5bf6e5fe/00-x-upload/video/101959664_922a548016bf6d6bc87dcb3b1ebfdbdc_KA7iHZ5u.mp4", "5天魔法英语特训营3.mp4"],
            ["https://dws-video.wenzaizhibo.com/484c98921f9b93af3e0c6cec973091a0/5bf6e617/00-x-upload/video/101964932_7d43e8e08e682935005c907429c40d93_Q9aRyDY6.mp4", "5天魔法英语特训营4.mp4"]]


def download_file(url_index):
    r = requests.get(url_list[url_index][0], stream=True)
    with open(url_list[url_index][1], "wb") as mp4:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                mp4.write(chunk)
    print(url_list[url_index][1], " 下载完成")


if __name__ == "__main__":
    print("start")
    threads = []
    url_index = 0
    for item in url_list:
        threads.append(threading.Thread(target=download_file, args=(url_index, )))
        url_index += 1
    for t in threads:
        t.setDaemon(True)
        t.start()
    # 必须等待for循环里面的所有线程都结束后，再执行主线程
    for k in threads:
        k.join()
    print("All threading finished!")
    print("end")
