from collections import Counter
import streamlit as st
from PIL import Image
import os
st.set_page_config(layout="centered", page_title="在线投票系统")
sysmenu = '''
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
'''
st.markdown(sysmenu,unsafe_allow_html=True)
with st.sidebar.expander('参评作品上传'):
    contain = st.container()
    contain.info('文件名为：类型作者作品名，扩展名必须是“jpg”，“png”')
    files = contain.file_uploader('选择文件上传',type=['jpg','png'],accept_multiple_files=True)
    if files:
        for file in files:
            if file.name.split('.')[1] in ['jpg','png','JPG','PNG']:
                data = Image.open(file)
                data.save(f'./image/{file.name}')
            else:
                contain.warning('上传文件类型错误！')

st.title('作品票选系统')
st.info('说明：分植物、动物2类。每人一次投票机会且投票总数不超过8张！')
with st.form('票选'):
    col1,col2 =st.columns(2)
    name = col1.text_input('投票人：')
    dept = col2.text_input('投票人所属机构：')
    col3,col4 = st.columns(2)
    but,info = st.columns(2)
    col3.header('您投票的作品：')
    col4.empty()
    commit  = but.form_submit_button('投票确认')
    tp_files = os.listdir('./image')
    sel_item = []
    for tp_file in tp_files:
        if st.checkbox(f'投票给{tp_file.split(".")[0]}'):
            sel_item.append(tp_file)
        else:
            sel_item.append('')
        st.image('./image/'+tp_file)
    if commit:
        if (len(name) == 0) | (len(dept) == 0):
            info.error('投票人与部门不允许为空！')
        else:
            with open('toupiao.txt','r') as f:
                users = []
                for lines in f.readlines():
                    users.append(lines.strip().split(',')[0])
            if name in users:
                # strs = ''
                info.error(f'{name}已经投过，谢谢！')
            elif 0< len([sel for sel in sel_item if sel != '']) <= 8:
                info.success('投票成功，谢谢！')
                strs = ''.join(sel + ',' for sel in sel_item if sel !='')
                with open('toupiao.txt','a') as f:
                    f.write(f'{name},{dept},' + strs + '\n')
                col4.success(strs)
                st.balloons()

                with st.sidebar.expander('投票结果统计'):
                    contain = st.container()
                    contain.info('票选结果：')
                    with open('toupiao.txt','r') as f:
                        users = []
                        # count_users = []
                        for lines in f.readlines():
                            users += lines.strip().split(',')[2:-1]
                    count = Counter(users)
                    for i in count.most_common(len(count)):
                        st.success(f'{i[0]},总计得票：{i[1]}\n')

            else:
                info.warning('票选有误，每人允许投票1~8张！')