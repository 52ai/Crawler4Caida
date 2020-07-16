# coding:utf-8
"""
create on July 16, 2020 by Wenyan YU
Email: ieeflsyu@outlook.com

Function:

探索性的研究手势操控，借助鼠标或键盘操作，确实是可以省去更多接口开发的麻烦
参考：https://github.com/moadmmh/Virtual-Mouse-Using-Gesture-Recognition
效果一般

opencv-python, 3.4.3.18

"""

import cv2
import numpy as np
from pynput.mouse import Button, Controller
import wx

mouse = Controller()

app = wx.App(False)
(sx, sy) = wx.GetDisplaySize()
(camx, camy) = (320, 240)
cap = cv2.VideoCapture(0)
cap.set(3, camx)
cap.set(4, camy)

# range for HSV (green color)
lower_g = np.array([33, 70, 30])
upper_g = np.array([102, 255, 255])

# Kerenel
kernelOpen = np.ones((5, 5))
kernelClose = np.ones((20, 20))

mLocOld = np.array([0, 0])
mouseLoc = np.array([0, 0])

DampingFactor = 2  # Damping factor must be greater than 1

isPressed = 0
openx, openy, openw, openh = (0, 0, 0, 0)

while True:

    ret, img = cap.read()

    img = cv2.resize(img, (340, 220))
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHSV, lower_g, upper_g)

    # using morphology to erase noise as maximum as possible
    new_mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
    another_mask = cv2.morphologyEx(new_mask, cv2.MORPH_CLOSE, kernelClose)
    final_mask = another_mask

    im2, conts, h = cv2.findContours(final_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Once 2 objects are detected the center of there distance will be the reference on controlling the mouse
    if (len(conts) == 2):

        # if the button is pressed we need to release it first
        if (isPressed == 1):
            isPressed = 0
            mouse.release(Button.left)

        # drawing the rectagle around both objects
        x1, y1, w1, h1 = cv2.boundingRect(conts[0])
        x2, y2, w2, h2 = cv2.boundingRect(conts[1])
        cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1), (255, 0, 0), 2)
        cv2.rectangle(img, (x2, y2), (x2 + w2, y2 + h2), (255, 0, 0), 2)

        # the line between the center of the previous rectangles
        cx1 = int(x1 + w1 / 2)
        cy1 = int(y1 + h1 / 2)
        cx2 = int(x2 + w2 / 2)
        cy2 = int(y2 + h2 / 2)
        cv2.line(img, (cx1, cy1), (cx2, cy2), (255, 0, 0), 2)

        # the center of that line (reference point)
        clx = int((cx1 + cx2) / 2)
        cly = int((cy1 + cy2) / 2)
        cv2.circle(img, (clx, cly), 2, (0, 0, 255), 2)

        # adding the damping factor so that the movement of the mouse is smoother
        mouseLoc = mLocOld + ((clx, cly) - mLocOld) / DampingFactor
        mouse.position = (sx - int((mouseLoc[0] * sx) / camx), int((mouseLoc[1] * sy) / camy))
        while mouse.position != (sx - int((mouseLoc[0] * sx) / camx), int((mouseLoc[1] * sy) / camy)):
            pass

        # setting the old location to the current mouse location
        mLocOld = mouseLoc

        # these variables were added so that we get the outer rectangle that combines both objects
        openx, openy, openw, openh = cv2.boundingRect(
            np.array([[[x1, y1], [x1 + w1, y1 + h1], [x2, y2], [x2 + w2, y2 + h2]]]))

    # when there's only when object detected it will act as a left click mouse
    elif (len(conts) == 1):
        x, y, w, h = cv2.boundingRect(conts[0])

        # we check first and we allow the press fct if it's not pressed yet
        # we did that to avoid the continues pressing
        if (isPressed == 0):

            if (abs((w * h - openw * openh) * 100 / (
                    w * h)) < 30):  # the difference between th combined rectangle for both objct and the
                isPressed = 1  # the outer rectangle is not more than 30%
                mouse.press(Button.left)
                openx, openy, openw, openh = (0, 0, 0, 0)

        # this else was added so that if there's only one object detected it will not act as a mouse
        else:
            # getting rectangle coordinates and drawing it
            x, y, w, h = cv2.boundingRect(conts[0])
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # getting the center of the circle that will be inside the outer rectangle
            cx = int(x + w / 2)
            cy = int(y + h / 2)
            cv2.circle(img, (cx, cy), int((w + h) / 4), (0, 0, 255), 2)  # drawing that circle

            mouseLoc = mLocOld + ((cx, cy) - mLocOld) / DampingFactor
            mouse.position = (sx - int((mouseLoc[0] * sx) / camx), int((mouseLoc[1] * sy) / camy))
            while mouse.position != (sx - int((mouseLoc[0] * sx) / camx), int((mouseLoc[1] * sy) / camy)):
                pass
            mLocOld = mouseLoc

    # showing the results
    cv2.imshow("Virtual mouse", img)

    # waiting for 'W' to be pressed to quit
    if cv2.waitKey(1) & 0xFF == ord('w'):
        break

cap.release()
cv2.destroyAllWindows()