# coding: utf-8
"""
create on Jun 21, 2021 By Wenyan YU
Email: ieeflsyu@outlook.com

Function：

探索Python自动化剪辑视频的方式
"""
from moviepy.editor import *


# 剪辑50-60秒的音乐00:00:50-00:00:60
clip = VideoFileClip("../000LocalData/MovieCut/Moviepy_Sample.mp4").subclip(60, 70)
# 降低音量
clip = clip.volumex(0.8)
# 生成一个clip
txt_clip = TextClip("MY FIRST MOVIE CUT, 20210621", fontsize=24, color='white')
# 字幕放置的位置和时间
txt_clip = txt_clip.set_position('bottom').set_duration(10)
# 将字幕clip，叠加到视频上
video_cut = CompositeVideoClip([clip, txt_clip])
# 写入编辑完成的音乐
video_cut.write_videofile("../000LocalData/MovieCut/done.mp4")
