import streamlit as st
import pymysql

st.set_page_config(page_title="基于Streamlit的登录、注册、注销功能演示",layout="wide")

con = pymysql.connect(host="192.168.136.128", user="root", password="111001125", database="pets", charset="utf8")

c = con.cursor()


def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)')


def add_userdata(username, password):
    if c.execute('SELECT username FROM userstable WHERE username = %s',(username)):
        st.warning("用户名已存在，请更换一个新的用户名。")
    else:
        c.execute('INSERT INTO userstable(username,password) VALUES(%s,%s)',(username,password))
        con.commit()
        st.success("恭喜，您已成功注册。")
        st.info("请在左侧选择“登录”选项进行登录。")


def login_user(username,password):
    if c.execute('SELECT username FROM userstable WHERE username = %s',(username)):
        c.execute('SELECT * FROM userstable WHERE username = %s AND password = %s',(username,password))
        data=c.fetchall()
        return data
    else:
        st.warning("用户名不存在，请先选择注册按钮完成注册。")


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data


def main():
    menu = ["首页","登录","注册", "注销"]

    if 'count' not in st.session_state:
        st.session_state.count = 0

    choice = st.sidebar.selectbox("选项",menu)
    st.sidebar.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 250px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 250px;
        margin-left: -250px;
    }
    </style>
    """,
    unsafe_allow_html=True,)

    if choice =="首页":
        st.subheader("首页")
        st.markdown('''Streamlit文档的地址是：https://docs.streamlit.io/''')
        c1, c2 = st.columns(2)
        with c1:
            st.success('''Streamlit中文公众号名称是：Streamlit, 公众号二维码如下''')
            st.image("sunrise.png")
        with c2:
            st.success('''Streamlit中文交流群二维码如下''')
            st.image("sunrise.png")

    elif choice =="登录":
        st.sidebar.subheader("登录区域")

        username = st.sidebar.text_input("用户名")
        password = st.sidebar.text_input("密码",type = "password")
        if st.sidebar.checkbox("开始登录"):
            logged_user = login_user(username,password)
            if logged_user:

                st.session_state.count += 1

                if st.session_state.count >= 1:

                    st.sidebar.success("您已登录成功，您的用户名是 {}".format(username))

                    st.title("成功登录后可以看到的内容")
                    st.balloons()
                    c1, c2 = st.columns(2)
                    with c1:
                        st.success('''Streamlit中文公众号名称是：Streamlit, 公众号二维码如下''')
                        st.image("sunrise.png")
                    with c2:
                        st.success('''Streamlit中文交流群二维码如下''')
                        st.image("sunrise.png")
            else:
                st.sidebar.warning("用户名或者密码不正确，请检查后重试。")

    elif choice =="注册":
        st.subheader("注册")
        new_user = st.sidebar.text_input("用户名")
        new_password = st.sidebar.text_input("密码",type = "password")

        if st.sidebar.button("注册"):
            create_usertable()
            add_userdata(new_user,new_password)

    elif choice =="注销":
        st.session_state.count = 0
        if st.session_state.count == 0:
            st.info("您已成功注销，如果需要，请选择左侧的登录按钮继续登录。")


if __name__=="__main__":
    main()