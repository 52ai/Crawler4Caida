# coding:utf-8
"""
create on Jan 24, 2022 By Wenyan YU

Function:

My first data web app using Streamlit

"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import datetime
from PIL import Image
import time
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth

st.set_page_config(
     page_title="MachineEyes",
     page_icon="http://www.mryu.top/yun.ico",
     layout="centered",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'http://www.mryu.top/',
         'Report a bug': "http://www.mryu.top/",
         'About': "MachineEyes v1.0. Eyes of the Machine Senses Everything of Network.This app is developed by Wayne YU."
     }
 )

with st.sidebar:
    selected = option_menu(
        "",
        ["48hours", "Monthly", "Archive", 'Visualization', 'User'],
        icons=['alarm', 'calendar2-month', "list-task", 'graph-up-arrow', 'heart'],
        menu_icon="cast",
        default_index=0)

# Session Initialization
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None


st.session_state.menu = selected
st.write("You select %s Menu" % selected)
# st.write("Session:", st.session_state)

names = ['John Smith', 'Rebecca Briggs']
usernames = ['jsmith', 'rbriggs']
passwords = ['123', '456']
hashed_passwords = stauth.hasher(passwords).generate()
authenticator = stauth.authenticate(names, usernames, hashed_passwords,
                                    'some_cookie_name', 'some_signature_key', cookie_expiry_days=30)
name, authentication_status = authenticator.login('login', 'sidebar')
if authentication_status:
    st.sidebar.write('Welcome *%s*' % name)
elif authentication_status is False:
    st.sidebar.error("Username/password is incorrect")
elif authentication_status is None:
    st.sidebar.warning("Please enter your username and password.")


if selected == '48hours':
    with st.expander("2022-01-25T09:14:39+00:00", True):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("Yemeni internet has been restored after a four-day outage")
            st.write("Yemen’s internet has been restored after a four-day outage. Internet service has been disrupted as a result of strikes on a telecommunications facility in Hudaydah by a Saudi-led coalition. Yemeni capital SANAA According to local residents, Internet service was restored in Yemen early Tuesday after a four-day outage. After Saudi-led coalition airstrikes targeted a telecommunications [...]")
            st.write("https://infosurhoy.com/news/yemeni-internet-has-been-restored-after-a-four-day-outage/")
        with col2:
            st.image("https://infosurhoy.com/wp-content/uploads/newsimages1/thumbs_b_c_bb407951ff2ea006e84dbbbbbaaab1ba.jpg")
            if st.button('like', key=1):
                st.write('Great!')
            st.write("BGP Monitor State")
            st.write("Performance ")
            st.write("Rate")

    with st.expander("2022-01-26T11:03:09+00:00", True):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("What happened with the Apple iCloud outage?")
            st.write("Panicked users took to Twitter wondering if their accounts had been hacked before the company confirmed it was an outage.The post What happened with the Apple ID outage? appeared first on Silicon Republic.")
            st.write("https://www.siliconrepublic.com/enterprise/apple-outage-id-icloud-down")
        with col2:
            st.image("https://www.siliconrepublic.com/wp-content/uploads/2022/01/icloud-718x523.jpeg")
            if st.button('like', key=2):
                st.write('Great!')
            st.write("BGP Monitor State")
            st.write("Performance")
            st.write("Rate")

    with st.expander("2022-01-24T15:54:43+00:00", True):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("Snowbound Regions of Greece Face Power Outages")
            st.write("The heavy snowfall in Greece brought about by the storm “Elpis” may cause power outages across regions that have been hit with dense snow. Many regions in Attica, where the city of Athens is located, Evia, and Crete are facing potential power outages due to the snow. Heavy snow causes power outages in Greece According […]Read the full story on GreekReporter.com.")
            st.write("https://greekreporter.com/2022/01/24/snow-greece-power-outage/")
        with col2:
            st.image("https://greekreporter.com/wp-content/uploads/2022/01/athens-snow2-credit-greek-reporter.jpg")
            if st.button('like', key=3):
                st.write('Great!')
            st.write("BGP Monitor State")
            st.write("Performance")
            st.write("Rate")

    with st.expander("2022-01-24T15:54:43+00:00", True):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("Yemeni internet has been restored after a four-day outage")
            st.write("Yemen’s internet has been restored after a four-day outage. Internet service has been disrupted as a result of strikes on a telecommunications facility in Hudaydah by a Saudi-led coalition. Yemeni capital SANAA According to local residents, Internet service was restored in Yemen early Tuesday after a four-day outage. After Saudi-led coalition airstrikes targeted a telecommunications [...]")
            st.write("https://infosurhoy.com/news/yemeni-internet-has-been-restored-after-a-four-day-outage/")
        with col2:
            st.image("https://infosurhoy.com/wp-content/uploads/newsimages1/thumbs_b_c_bb407951ff2ea006e84dbbbbbaaab1ba.jpg")
            if st.button('like', key=4):
                st.write('Great!')
            st.write("BGP Monitor State")
            st.write("Performance")
            st.write("Rate")

    with st.expander("2022-01-24T15:54:43+00:00", True):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("What happened with the Apple iCloud outage?")
            st.write("Panicked users took to Twitter wondering if their accounts had been hacked before the company confirmed it was an outage.The post What happened with the Apple ID outage? appeared first on Silicon Republic.")
            st.write("https://www.siliconrepublic.com/enterprise/apple-outage-id-icloud-down")
        with col2:
            st.image("https://www.siliconrepublic.com/wp-content/uploads/2022/01/icloud-718x523.jpeg")
            if st.button('like', key=5):
                st.write('Great!')
            st.write("BGP Monitor State")
            st.write("Performance")
            st.write("Rate")

    with st.expander("2022-01-24T15:54:43+00:00", True):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("Snowbound Regions of Greece Face Power Outages")
            st.write("The heavy snowfall in Greece brought about by the storm “Elpis” may cause power outages across regions that have been hit with dense snow. Many regions in Attica, where the city of Athens is located, Evia, and Crete are facing potential power outages due to the snow. Heavy snow causes power outages in Greece According […]Read the full story on GreekReporter.com.")
            st.write("https://greekreporter.com/2022/01/24/snow-greece-power-outage/")
        with col2:
            st.image("https://greekreporter.com/wp-content/uploads/2022/01/athens-snow2-credit-greek-reporter.jpg")
            if st.button('like', key=6):
                st.write('Great!')
            st.write("BGP Monitor State")
            st.write("Performance")
            st.write("Rate")

    with st.expander("2022-01-24T15:54:43+00:00", True):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("Yemeni internet has been restored after a four-day outage")
            st.write("Yemen’s internet has been restored after a four-day outage. Internet service has been disrupted as a result of strikes on a telecommunications facility in Hudaydah by a Saudi-led coalition. Yemeni capital SANAA According to local residents, Internet service was restored in Yemen early Tuesday after a four-day outage. After Saudi-led coalition airstrikes targeted a telecommunications [...]")
            st.write("https://infosurhoy.com/news/yemeni-internet-has-been-restored-after-a-four-day-outage/")
        with col2:
            st.image("https://infosurhoy.com/wp-content/uploads/newsimages1/thumbs_b_c_bb407951ff2ea006e84dbbbbbaaab1ba.jpg")
            if st.button('like', key=7):
                st.write('Great!')
            st.write("BGP Monitor State")
            st.write("Performance")
            st.write("Rate")

    with st.expander("2022-01-24T15:54:43+00:00", True):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("What happened with the Apple iCloud outage?")
            st.write("Panicked users took to Twitter wondering if their accounts had been hacked before the company confirmed it was an outage.The post What happened with the Apple ID outage? appeared first on Silicon Republic.")
            st.write("https://www.siliconrepublic.com/enterprise/apple-outage-id-icloud-down")
            st.write("2022-01-26T11:03:09+00:00")
        with col2:
            st.image("https://www.siliconrepublic.com/wp-content/uploads/2022/01/icloud-718x523.jpeg")
            if st.button('like', key=8):
                st.write('Great!')
            st.write("BGP Monitor State")
            st.write("Performance")
            st.write("Rate")

    with st.expander("2022-01-24T15:54:43+00:00", True):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("Snowbound Regions of Greece Face Power Outages")
            st.write("The heavy snowfall in Greece brought about by the storm “Elpis” may cause power outages across regions that have been hit with dense snow. Many regions in Attica, where the city of Athens is located, Evia, and Crete are facing potential power outages due to the snow. Heavy snow causes power outages in Greece According […]Read the full story on GreekReporter.com.")
            st.write("https://greekreporter.com/2022/01/24/snow-greece-power-outage/")
            st.write("2022-01-24T15:54:43+00:00")
        with col2:
            st.image("https://greekreporter.com/wp-content/uploads/2022/01/athens-snow2-credit-greek-reporter.jpg")
            if st.button('like', key=9):
                st.write('Great!')
            st.write("BGP Monitor State")
            st.write("Performance")
            st.write("Rate")
elif selected == "User":
    pass
else:
    pass

