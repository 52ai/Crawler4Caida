import cv2
import mediapipe as mp
import streamlit as st
import time


st.set_page_config(page_title="手掌识别", layout="wide")
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
Draw = mp.solutions.drawing_utils
point_style = Draw.DrawingSpec(color=(0, 0, 255), thickness=5)
line_style = Draw.DrawingSpec(color=(0, 255, 0), thickness=10)
time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


for x in range(3):
    ret, img = cap.read()
    if ret:
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(imgRGB)
        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                Draw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS, point_style, line_style)

        cv2.putText(img, f"{time_str}", (30, 50), cv2.FONT_ITALIC, 0.5, (255, 0, 0), 2)
        c1, c2, c3 = st.columns([0.1, 1, 1])
        with c1:
            st.empty()
        with c2:
            st.image(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
            time.sleep(0.1)
        with c3:
            st.image(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
            time.sleep(0.1)
