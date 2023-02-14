import cv2
import mediapipe as mp
import time
import math

cam = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils


def CordGetter(landmark,*axis):
    x = cords[0].landmark[landmark].x
    y = cords[0].landmark[landmark].y
    if axis[0].lower() == "x":
        return x
    if axis[0].lower() == "y":
        return y
    return [x, y]


while True:
    success, img = cam.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    cords = results.multi_hand_landmarks  # hand cords (x,y,z)
    if cords:
        for Hand in cords:
            mpDraw.draw_landmarks(img, Hand, mpHands.HAND_CONNECTIONS)  # draws the hand no cords
            resX = cv2.getWindowImageRect('Image')[2]
            resY = cv2.getWindowImageRect('Image')[3]
    cv2.imshow("Image", cv2.flip(img, 1))
    cv2.waitKey(1)
