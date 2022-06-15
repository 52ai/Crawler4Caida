import streamlit as st
import pymysql

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
    layout="centered",
)

sysmenu = '''
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
'''
st.markdown(sysmenu, unsafe_allow_html=True)

with st.sidebar:
    st.sidebar.markdown(
        """
        <small> ET-GIM 0.1.0 | Jane 2022 </small>  
        [<img src='http://www.mryu.top/content/templates/start/images/github.png' class='img-fluid' width=25 height=25>](https://github.com/52ai) 
        [<img src='http://www.mryu.top/content/templates/start/images/weibo.png' class='img-fluid' width=25 height=25>](http://weibo.com/billcode) 
         """,
        unsafe_allow_html=True,
    )

if 'count' not in st.session_state:
    st.session_state.count = 0

st.info("ET-GIM入口")

# st.session_state['login_status'] = True
pymysql_info_file = "D:/Code/Crawler4Caida/.streamlit/pymysql_info.txt"
with open(pymysql_info_file, 'r', encoding='utf-8') as f:
    line = f.readlines()[0]
    line = line.strip().split(",")
    con = pymysql.connect(host=line[0], user=line[1], password=line[2], database=line[3], charset="utf8")
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
        st.info("请选择“登录”选项进行登录。")


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


menu = ["首页","登录","注册", "注销"]
choice = st.selectbox("", menu)

if choice == "首页":
    st.write("# Welcome to Streamlit! 👋")
    st.sidebar.success("Select a demo above.")
    st.write("Session:", st.session_state)

    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.
        **👈 Select a demo from the sidebar** to see some examples
        of what Streamlit can do!
        ### Want to learn more?
        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
            forums](https://discuss.streamlit.io)
        ### See more complex demos
        - Use a neural net to [analyze the Udacity Self-driving Car Image
            Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )

elif choice == "登录":
    st.subheader("登录区域")

    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")
    if st.checkbox("开始登录"):
        logged_user = login_user(username, password)
        if logged_user:
            st.session_state.count += 1
            if st.session_state.count >= 1:
                st.success("您已登录成功，您的用户名是 {}".format(username))

                st.info("成功登录后可以看到气球")
                st.balloons()
        else:
            st.warning("用户名或者密码不正确，请检查后重试。")

elif choice == "注册":
    st.subheader("注册")
    new_user = st.text_input("用户名")
    new_password = st.text_input("密码", type="password")

    if st.button("注册"):
        create_usertable()
        add_userdata(new_user, new_password)

elif choice == "注销":
    st.session_state.count = 0
    if st.session_state.count == 0:
        st.info("您已成功注销，如果需要，请选择登录按钮继续登录。")

