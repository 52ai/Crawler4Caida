# coding:utf-8
"""
create on June 17, 2022, By Wayne YU
Email: ieeflsyu@outlook.com

Function:

该程序是ET-GIM项目的入口程序

"""
import streamlit as st
import pymysql

st.set_page_config(
    page_title="ET-GIM",
    page_icon="world_map",
    layout="centered",
    initial_sidebar_state="auto"
)

# 去除streamlit的原生标记
sys_menu = '''
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
'''
st.markdown(sys_menu, unsafe_allow_html=True)

# st.write(st.session_state)


if 'count' not in st.session_state:
    st.session_state.count = 0
    st.session_state.user = "Guest"


# 给侧边栏添加APP版本信息
with st.sidebar:
    st.write("Login:", st.session_state.user)
    st.sidebar.markdown(
        """
        <small> ET-GIM 0.1.0 | Jane 2022 </small>  
        [<img src='http://www.mryu.top/content/templates/start/images/github.png' class='img-fluid' width=25 height=25>](https://github.com/52ai) 
        [<img src='http://www.mryu.top/content/templates/start/images/weibo.png' class='img-fluid' width=25 height=25>](http://weibo.com/billcode) 
         """,
        unsafe_allow_html=True,
    )

# 读取本地Mysql信息
pymysql_info_file = "D:/Code/Crawler4Caida/.streamlit/pymysql_info.txt"
with open(pymysql_info_file, 'r', encoding='utf-8') as f:
    line = f.readlines()[0]
    line = line.strip().split(",")
    con = pymysql.connect(host=line[0], user=line[1], password=line[2], database=line[3], charset="utf8")
c = con.cursor()


# 以下为用户管理的Mysql操作函数，注册、登录、退出
def create_user_table():
    """
    新建用户表
    :return:
    """
    c.execute('CREATE TABLE IF NOT EXISTS users_table(username TEXT, password TEXT)')


def add_userdata(username, password):
    if c.execute('SELECT username FROM users_table WHERE username = %s', username):
        st.warning("用户名已存在，请更换一个新的用户名。")
    else:
        c.execute('INSERT INTO users_table(username,password) VALUES(%s,%s)', (username, password))
        con.commit()
        st.success("恭喜，您已成功注册。")
        st.info("请选择“登录”选项进行登录。")


def login_user(username, password):
    if c.execute('SELECT username FROM users_table WHERE username = %s', username):
        c.execute('SELECT * FROM users_table WHERE username = %s AND password = %s', (username, password))
        data = c.fetchall()
        return data
    else:
        st.warning("用户名不存在，请先选择注册按钮完成注册。")


def view_all_users():
    c.execute('SELECT * FROM users_table')
    data = c.fetchall()
    return data


menu = ["首页", "登录", "注册", "注销"]
choice = st.selectbox("", menu)

if choice == "首页":

    # st.image("./image/fore_cn_2020_gao(1).png", caption="中国自治域网络互联地图(2020)")
    # st.image("./image/fore_cjk_2020_gao.png", caption="中日韩网络互联关系地图")
    st.image("./image/canvas2019_top200.png", caption="全球TOP200网络互联关系地图")

    st.write("# Welcome to ET-GIM! 😁")
    st.markdown(
        """
        ET-GIM，即工程技术-全球网络地图（Engineering Technology-Global Internet Map）的英文缩写。
        它脱胎于院2022年度的**工程技术课题**。  
        ET-GIM的设计开发理念是 **“快速形成一版最小可用系统”** ，交付至工程技术课题项目组。 
        ET-GIM系统的主要功能可概括为 **“4+1”**，即政策层、物理层、逻辑层、应用层4张地图，1项可视化探索。         
        ### 产品受众
        政府部门、走出去企业、面向公众用户及相关单位  
        ### 产品优点
        - 多层网络地图整合
        - 可自定义数据规则
        - 具备多需求的网络地图数据挖掘能力，可有效支撑国际网络分析及相关报告撰写
        
        >create on June 17, 2022, By Wayne YU  
        >Email: ieeflsyu@outlook.com  
        >Github: https://github.com/52ai
    """
    )

elif choice == "登录":
    st.subheader("登录区域")
    username_in = st.text_input("用户名")
    password_in = st.text_input("密码", type="password")
    if st.button("开始登录"):
        logged_user = login_user(username_in, password_in)
        if logged_user:
            st.session_state.count += 1
            if st.session_state.count >= 1:
                st.success("您已登录成功，您的用户名是 {}".format(username_in))
                st.info("成功登录后可以看到气球")
                st.session_state.user = username_in
                st.balloons()
        else:
            st.warning("用户名或者密码不正确，请检查后重试。")

elif choice == "注册":
    st.subheader("注册")
    new_user = st.text_input("用户名")
    new_password = st.text_input("密码", type="password")

    if st.button("注册"):
        create_user_table()
        add_userdata(new_user, new_password)

elif choice == "注销":
    st.session_state.count = 0
    st.session_state.user = "Guest"
    if st.session_state.count == 0:
        st.info("您已成功注销，如果需要，请选择登录按钮继续登录。")
