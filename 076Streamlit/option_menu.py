import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
import pandas as pd
import numpy as np
import requests
import json
import re
import langid

st.set_page_config(page_title="Global Internet Map", page_icon="💖", layout="wide")

sysmenu = '''
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
'''

st.markdown(sysmenu,unsafe_allow_html=True)

with st.sidebar:
    choose = option_menu("GIM", ["介绍", "图片/音乐/视频", "数据可视化", "翻译", "地理", "其他应用"],
                         icons=['house', 'file-earmark-music', 'bar-chart', 'translate', 'brightness-high'],
                         menu_icon="broadcast", default_index=0)

if choose == "介绍":
    col1, col2 = st.columns(2)
    with col1:
        st.image("./image/fore_cn_2020_gao(1).png", caption="中国自治域网络互联地图")
    with col2:
        st.image("./image/fore_us_2020_gao.png", caption="美国自治域网络互联地图")
        st.write("微信公众号Streamlit由作者创建已由半年多。\n\n\n\n"
                 "主题就是为大家分享Python与Streamlit结合的各种案例，用于提高大家的办公效率。\n\n\n\n"
                 "一个人可以走的很快，一群人可以走的更远。\n\n\n"
                 "为了让大家一起进步，由此创建了一个微信讨论群，可以扫下方二维码添加作者微信\n\n\n"
                 "验证信息：我来自公众号Streamlit")

elif choose == "图片/音乐/视频":
    selecte1 = option_menu(None, ["图片", "音乐", "视频"],
        icons=['house', 'cloud-upload', "list-task"],
        menu_icon="cast", default_index=0, orientation="horizontal")

    if selecte1 == "图片":
        with st.container():
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.image("./image/Mayavi_3d.png")
            with col2:
                st.image("./image/Mayavi_3d.png")
            with col3:
                st.image("./image/Mayavi_3d.png")
            with col4:
                st.image("./image/Mayavi_3d.png")
        with st.container():
            st.image("./image/fore_us_2020_gao.png")
    elif selecte1 == "音乐":
        st.audio("The Sounds Of Silence.mp3")
    elif selecte1 == "视频":
        st.video("star.mp4")

elif choose == "数据可视化":
    selecte2 = option_menu(None, ["Echarts", "Plotly", "Streamlit-apex-charts"],
                           icons=['house', 'cloud-upload', "list-task"],
                           menu_icon="cast", default_index=0, orientation="horizontal")

    df = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
        columns=['lat', 'lon'])

    if selecte2 == "Echarts":
        # html.iframe("https://mp.weixin.qq.com/s/5VDGsnpgx8iF90aF7p1yMg")
        st.map(df)

    elif selecte2 == "Plotly":
        # html.iframe("https://mp.weixin.qq.com/s/ckcDXhoRmxlxswOviQUbFg")
        st.map(df)

    elif selecte2 == "Streamlit-apex-charts":
        # st.components.v1.iframe("https://mp.weixin.qq.com/s/Sm3UifwoxVKTsMD-rsyovA")
        st.map(df)

elif choose == "翻译":
    selecte3 = option_menu(None, ["单词翻译", "谷歌翻译"],
                           icons=['house', 'cloud-upload'],
                           menu_icon="cast", default_index=0, orientation="horizontal")
    if selecte3 == "单词翻译":
        # html.iframe("https://mp.weixin.qq.com/s/6lYXgMLlkELETB4YAIScFQ")
        st.header("中英单词互翻神器")
        st.info("要翻译中文单词，请输入中文，会返回对应英文；\n\n\n\n要翻译英文单词，请输入英文，会返回对应中文;")
        danci = st.text_input("请输入要查找的中文单词或英文单词")
        fanhui = requests.get("http://dict.iciba.com/dictionary/word/suggestion?word=" + danci)
        data1 = fanhui.text
        data2 = json.loads(data1)
        for i in range(len(data2["message"])):
            st.write(data2["message"][i]["key"], data2["message"][i]["paraphrase"])

    elif selecte3 == "谷歌翻译":
        # html.iframe("https://mp.weixin.qq.com/s/8V72xwGWcdIk4G_d_pLPTQ")
        def translate(text, target_language, key):
            url = 'https://translate.google.cn/_/TranslateWebserverUi/data/batchexecute?rpcids=MkEWBc&f.sid=-2984828793698248690&bl=boq_translate-webserver_20201221.17_p0&hl=zh-CN&soc-app=1&soc-platform=1&soc-device=1&_reqid=5445720&rt=c'
            headers = {
                'origin': 'https://translate.google.cn',
                'referer': 'https://translate.google.cn/',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
                'x-client-data': 'CIW2yQEIpbbJAQjEtskBCKmdygEIrMfKAQj2x8oBCPfHygEItMvKAQihz8oBCNzVygEIi5nLAQjBnMsB',
                'Decoded': 'message ClientVariations {repeated int32 variation_id = [3300101, 3300133, 3300164, 3313321, 3318700, 3318774, 3318775, 3319220, 3319713, 3320540, 3329163, 3329601];}',
                'x-same-domain': '1'
            }
            data = {
                'f.req': f'[[["MkEWBc","[[\\"{text}\\",\\"auto\\",\\"{target_language}\\",true],[null]]",null,"generic"]]]'}
            res = requests.post(url, headers=headers, data=data).text
            temp = re.findall(r'\\(.*?)\\', res)
            # st.write(temp)
            yiwen = str(temp[key]).replace('"', '')
            return st.success(yiwen)

        st.header("多语种翻译工具")
        st.info("说明：输入中文得英文，输入英文得中文，输入韩语、日语、俄语、法语、葡萄牙语、西班牙语将得到中文")
        text = st.text_input("请输入你要翻译的内容,可输入中文或英文")

        if len(text) > 0:
            # st.write(langid.classify(text)[0])
            if langid.classify(text)[0] == "en":  # 英语
                translate(text, "zh", 3)
            elif langid.classify(text)[0] == "zh":  # 中文
                translate(text, "en", 3)
            elif langid.classify(text)[0] == "ko":  # 韩语
                translate(text, "zh", 4)
            elif langid.classify(text)[0] == "ja":  # 日语
                translate(text, "zh", 5)
            elif langid.classify(text)[0] == "ru":  # 俄语
                translate(text, "zh", 4)
            elif langid.classify(text)[0] == "fr":  # 法语
                translate(text, "zh", 4)
            elif langid.classify(text)[0] == "ku":  # 葡萄牙语
                translate(text, "zh", 4)
            elif langid.classify(text)[0] == "pt":  # 西班牙语
                translate(text, "zh", 4)

elif choose == "地理":
    selecte4 = option_menu(None, ["地震数据", "KML", "Mapinfo TAB"],
                           icons=['house', 'cloud-upload', 'cloud-upload'],
                           menu_icon="cast", default_index=0, orientation="horizontal")

    if selecte4 == "地震数据":
        # html.iframe("https://mp.weixin.qq.com/s/HwYQXotuyZAtecOY6SBYKw")
        st.image("sunrise.png")

    elif selecte4 == "KML":
        # html.iframe("https://mp.weixin.qq.com/s/-z3dLVE-K0ejB6Sye0EOhg")
        st.image("sunrise.png")

    elif selecte4 == "Mapinfo TAB":
        # html.iframe("https://mp.weixin.qq.com/s/kP731l40Rf61CTWfyqbQmg")
        st.image("sunrise.png")


elif choose == "其他应用":
    selecte5 = option_menu(None, ["Javascript", "展示PPT", "嵌入PDF"],
                           icons=['house', 'cloud-upload', "list-task"],
                           menu_icon="cast", default_index=0, orientation="horizontal")

    if selecte5 == "Javascript":
        # html.iframe("https://mp.weixin.qq.com/s/Sr4_IAK3pGWRLgjO51i8Mw")
        st.image("sunrise.png")

    elif selecte5 == "展示PPT":
        # html.iframe("https://mp.weixin.qq.com/s/i0VcKUHBCEHjoOYvoiGolQ")
        st.image("sunrise.png")

    elif selecte5 == "嵌入PDF":
        # html.iframe("https://mp.weixin.qq.com/s/W8DX74LZYdosDUXUIpoa1g")
        st.image("sunrise.png")
