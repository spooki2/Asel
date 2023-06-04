import base64
import hashlib
import inspect
import json
import socket
import sys
import threading
import time
import traceback

import sounddevice as sd
import cv2
import pyaudio
import numpy as np
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QImage, QPixmap

from AselClass import lastTalkedStack
from GUIcode import AlertGUI
from GUIcode import AselMainGUI
from GUIcode import IntroGUI
from GUIcode import LoginGUI
from GUIcode import RegisterGUI

# define a video capture object
# setup paths
chunks = 1024*2
killCameraEvent = threading.Event()
killCameraEvent.choice = False
vid = None
inputStream = None
outputStream = None
threadCall = None
activeCallUsername = ""
cameraToggle = True
cameraToggleSelf = True
camResolution = {'height': 0, 'width': 0}
callUsername = "<NAME>"
initCallGUI = False
activeChatData = ""
callPopUp = False
activeChatUser = "ben"  # TESTING: should be none
recv = ""
pyqtPixmap = None
skipToLogin = False
skipToRegister = False
registerPath = False
loginPath = False
registerSubmitPath = False
registerValid = False
loginValid = False
runAselPath = False
recentChats = lastTalkedStack(8)  # a custom class stack of all recent chats with the max value being set to 8


def listenThreadTCP():
    global recentChats
    while True:
        global callPopUp
        global callUsername
        global activeChatUser
        global initCallGUI
        # print(f'[PACKET GOT]: {recv.decode()}')
        # packet =""
        try:
            packet = json.loads(TCPclient.recv(90000).decode())
        except:
            print(f"[BAD PACKET]: {TCPclient.recv(90000).decode()}")
        try:
            if packet['registerValid']:
                global registerValid
                registerValid = True
        except:
            pass
        try:
            if packet['loginValid']:
                global loginValid
                loginValid = True
        except:
            pass
        try:

            if packet['request'] == "userLookup":
                if packet['username'] is None:
                    activeChatUser = None
                else:
                    activeChatUser = packet['username']
                    recentChats.push(activeChatUser)
                    refreshChat()
            elif packet['request'] == "loadChat":
                global activeChatData

                if activeChatUser == packet['from']:
                    activeChatData = formatChatData(json.dumps(packet))
                else:
                    print("[NOTIFICATION]")
            elif packet['request'] == "callPopup":
                callUsername = packet['caller']
                callPopUp = True

            elif packet['request'] == "wasCallAccepted":
                if packet['bool']:
                    print("[CALL ACCEPTED]")
                    initCallGUI = True
                else:
                    print("[CALL DECLINED]")
                    initCallGUI = False
            elif packet['request'] == "cameraToggle":
                global cameraToggle
                if packet['bool']:
                    cameraToggle = True
                if not packet['bool']:
                    cameraToggle = False
                print(f"other user camtoggle: {cameraToggle}")

            elif packet['request'] == "callEnded":
                initCallGUI = False
                killCameraEvent.choice = True




        except:
            # traceback.print_exc()
            pass


import wave


def micListenThread():
    filename = 'twoOfUs.wav'
    wf = wave.open(filename, 'rb')
    # data = wf.readframes(chunks)
    data, address = UDPclientMic.recvfrom(20000)
    oldData = data
    while True:
        data, address = UDPclientMic.recvfrom(chunks * 2)

        if data == None:
            print("NONe")
            # Open the file
        outputStream.write(data)
        oldData = data



def camListenThread():
    global pyqtPixmap
    global camResolution
    while True:
        try:
            data, address = UDPclientWebcam.recvfrom(90000)
            data = data.decode()
            decodedImg = imageDecode(data)
            height, width, channel = decodedImg.shape
            camResolution['height'] = height
            camResolution['width'] = width
            bytesPerLine = 3 * width

            # Convert the color space from BGR to RGB
            decodedImg = cv2.cvtColor(decodedImg, cv2.COLOR_BGR2RGB)
            pyqtImage = QImage(decodedImg.data, width, height, bytesPerLine, QImage.Format_RGB888)

            pyqtPixmap = QPixmap.fromImage(pyqtImage)  # converts to pyqt5 image
        except:
            print("[Bad Frame]")
            pass


def callPopupChoice(Choice, popupObject):
    data = {"request": "callPopupChoice", "acceptedCall": Choice, "UDPcamPort": UDPclientWebcam.getsockname()[1],
            "UDPmicPort": UDPclientMic.getsockname()[1]}
    TCPclient.send(json.dumps(data).encode())  # dict -> json[str]
    popupObject.close()


def formatChatData(jsonStr):
    # Parse the outer JSON string
    outer_json = json.loads(jsonStr)

    # Check if outer_json has "request" and "data" keys
    if "request" not in outer_json or "data" not in outer_json:
        return "Invalid JSON string"

    # Check if request is 'loadChat'
    if outer_json["request"] != "loadChat":
        return "Invalid request"

    # Split the data string into separate lines
    data_lines = outer_json["data"].split("\n")

    # For each line, parse the JSON and format the output
    formatted_data = []
    for line in data_lines:
        if line:
            # Parse the inner JSON string
            inner_json = json.loads(line)

            # Format the output
            formatted_line = f'{inner_json["sender"]}: {inner_json["message"]}'
            formatted_data.append(formatted_line)

    # Join the formatted data lines into a single string with newlines
    return "\n".join(formatted_data)


while True:
    try:
        ip = '10.0.0.23'
        port = 4000
        TCPclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCPclient.connect((ip, port))
        TCPclient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # makes port available after closing
        print(f"TCP connected on port {port}")

        # UDP client socket
        UDPclientWebcam = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDPclientWebcam.connect((ip, (port + 1)))
        UDPclientWebcam.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # makes port available after closing

        UDPclientMic = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDPclientMic.connect((ip, (port + 2)))
        UDPclientMic.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # makes port available after closing

        break

    except WindowsError:
        print("[Server Connection Failed]")
        print("retrying...\n")
        time.sleep(3)

threading.Thread(target=listenThreadTCP).start()
threading.Thread(target=camListenThread).start()
threading.Thread(target=micListenThread).start()
myUsername = "blank"


def regSubmit():
    global registerSubmitPath
    global myUsername
    registerSubmitPath = True
    username = RegisterGUI.username
    myUsername = username
    passwordHash = hashlib.sha256(RegisterGUI.password.encode()).hexdigest()
    data = {"request": "register", "username": username, "password": passwordHash}
    TCPclient.send((json.dumps(data)).encode())  # dict -> json[str]
    RegisterGUI.registerGlobal.close()


def logSubmit():
    username = LoginGUI.username
    passwordHash = hashlib.sha256(LoginGUI.password.encode()).hexdigest()
    data = {"request": "login", "username": username, "password": passwordHash}
    TCPclient.send(json.dumps(data).encode())  # dict -> json[str]
    LoginGUI.loginGlobal.close()


def regChoice():  # user chose register on intro
    global registerPath
    registerPath = True
    IntroGUI.introGlobal.close()


def logChoice():  # user chose login on intro
    global loginPath
    loginPath = True
    IntroGUI.introGlobal.close()


def okRegister():
    global skipToLogin
    global skipToRegister
    skipToRegister = False
    skipToLogin = True
    AlertGUI.alertGlobal.close()


def tryAgainRegister():
    global skipToLogin
    global skipToRegister
    skipToRegister = True
    skipToLogin = False
    AlertGUI.alertGlobal.close()


def okLogin():
    # run asel
    refreshChat()
    AlertGUI.alertGlobal.close()


def tryAgainLogin():
    global skipToLogin
    global skipToRegister
    skipToRegister = False
    skipToLogin = True
    AlertGUI.alertGlobal.close()


def execGUI(objectGUI, *callbacks):  # function that procedurally runs a GUI module and links its paramaters
    classGUI = inspect.getmembers(objectGUI, lambda member: inspect.isclass(member))
    classGUI = classGUI[0][1]
    app = objectGUI.QtWidgets.QApplication(sys.argv)
    Asel = objectGUI.QtWidgets.QMainWindow()
    classGUI().setupUi(Asel, *callbacks)
    Asel.show()
    app.exec_()


def sendDM(message):
    data = {"request": "dm", "target": activeChatUser, "message": message}
    if message == "" or message is None:
        data = {"request": "dm", "target": activeChatUser, "message": "blankMsg"}  # * testing
    TCPclient.send(json.dumps(data).encode())  # dict -> json[str]


# todo:  sqllite, encyrpted "diffie hellman",
# todo strechlist:  block 2 many requests, check both sides for illegal characters

def userLookup(customInput=None):
    if not customInput:
        # userSearch = AselMainGUI.userLookupName
        pass
    else:
        userSearch = customInput
        data = {"request": "userLookup", "username": userSearch}
        TCPclient.send((json.dumps(data)).encode())  # dict -> json[str]


def refreshLite():  # callback function that refreshes the chat with current active data
    _ = 0
    # recentChats.printStack()
    # print(recentChats.getList()[1])
    for friendBox in AselMainGUI.globalFriendBoxes:
        try:
            friendBox.setText(f"{recentChats.getList()[_]}")
        except IndexError:
            pass
        _ += 1

    AselMainGUI.globalTextBox.setPlainText(activeChatData)


def refreshChat():
    data = {"request": "loadChat", "target": activeChatUser}
    TCPclient.send((json.dumps(data)).encode())  # dict -> json[str]


def sendCallRequest():
    global callUsername
    callUsername = activeChatUser
    data = {"request": "call", "targetName": activeChatUser, "UDPcamPort": UDPclientWebcam.getsockname()[1],
            "UDPmicPort": UDPclientMic.getsockname()[1]}
    TCPclient.send((json.dumps(data)).encode())  # dict -> json[str]


def checkIfCalled():
    global callPopUp
    if callPopUp:
        AselMainGUI.AselMainGUIclass.callAlertInit(AselMainGUI.AselMainGUIclass, callPopupChoice, callUsername)
        callPopUp = False


runCallEndOnce = False  # the call cant end before it was even started


def checkIfCallEnded():
    global runCallStartOnce
    global runCallEndOnce
    if not initCallGUI:
        if AselMainGUI.globalStackedWidget.currentIndex() != 0:
            runCallEndOnce = True
        AselMainGUI.globalStackedWidget.setCurrentIndex(0)

        if runCallEndOnce:
            # callEnded = False
            print("kill camera")
            vid.release()
            # TODO ALL:
            # inputStream.stop()
            # inputStream.close()
            # outputStream.stop()
            # outputStream.close()
            # pyAudioIns.terminate()
            runCallStartOnce = False
            runCallEndOnce = False


runCallStartOnce = False


def initCallFunc():
    global threadCall
    global runCallStartOnce
    if initCallGUI:
        if not runCallStartOnce:
            AselMainGUI.globalStackedWidget.setCurrentIndex(1)
            threadCall = threading.Thread(target=callThreadFunc)
            threadCall.start()
            print("running once")
            runCallStartOnce = True


def imageEncode(frameImage, compVal):  # Convert the image to a base64 string
    camValidVal, buffer = cv2.imencode('.jpg', frameImage, [int(cv2.IMWRITE_JPEG_QUALITY), compVal])
    imgBytes = base64.b64encode(buffer)
    return imgBytes


def imageDecode(bytesImage):  # Convert the base64 string back to an image
    img_bytes = base64.b64decode(bytesImage)
    img_arr = np.frombuffer(img_bytes, dtype=np.uint8)
    decoded_img = cv2.imdecode(img_arr, flags=cv2.IMREAD_COLOR)
    return decoded_img


def callThreadFunc():
    # send microphone
    # microphone sample rate
    pyAudioIns = pyaudio.PyAudio()
    channels = 1
    rate = 48000
    Format = pyaudio.paInt16

    default_device_index = pyAudioIns.get_default_input_device_info()["index"]
    deviceInfo = pyAudioIns.get_device_info_by_index(default_device_index)
    channels = deviceInfo["maxInputChannels"]
    rate = int(deviceInfo["defaultSampleRate"])

    global inputStream
    global outputStream

    inputStream = pyAudioIns.open(format=Format, channels=channels, rate=rate, input=True, frames_per_buffer=chunks)
    outputStream = pyAudioIns.open(format=Format, channels=channels, rate=rate, output=True, frames_per_buffer=chunks)

    # Start video capture
    global vid

    vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    camWorks = True

    toggleLogic = False
    while initCallGUI:
        # print("len: ",len(inputStream.read(chunks)))
        UDPclientMic.send(inputStream.read(chunks))
        # print("sent mic data!")

        if cameraToggleSelf:
            camValid, frame = vid.read()
            if camValid:
                imgBytes = imageEncode(frame, 70)
                UDPclientWebcam.send(imgBytes)
            else:
                print("[CAM NOT VALID]")
        if cameraToggleSelf and toggleLogic:
            TCPclient.send(json.dumps(
                {"request": "relay", "requestRelay": "cameraToggle", "target": callUsername, "bool": True}).encode())
            toggleLogic = False
            print("sending True")
        if not cameraToggleSelf and not toggleLogic:
            TCPclient.send(json.dumps(
                {"request": "relay", "requestRelay": "cameraToggle", "target": callUsername, "bool": False}).encode())
            print("sending False")
            toggleLogic = True


# due to how pyqt5 works pythons garbage collector will automatically close windows that do not
# refer to themselves, thats why you can NOT- call PathController from a different function, a workaround to this is
# using "paths", which are booleans which will determine the flow of the menu's


def updateCamFeed(cameraToggleButton):
    global cameraToggleSelf
    cameraToggleSelf = cameraToggleButton
    try:
        if cameraToggle:
            AselMainGUI.globalWebCam.setGeometry(QtCore.QRect(0, 0, camResolution["width"], camResolution["height"]))
            AselMainGUI.globalWebCam.setPixmap(pyqtPixmap)
        else:
            AselMainGUI.globalWebCam.setGeometry(QtCore.QRect(100, 10, 341, 341))
            AselMainGUI.globalWebCam.setPixmap(QtGui.QPixmap(r"GUIcode\icons\cameraOff.png"))
    except:
        pass


def killCall():
    data = {"request": "killCall"}
    TCPclient.send(json.dumps(data).encode())


def pathController():
    if not skipToLogin and not skipToRegister:
        execGUI(IntroGUI, regChoice, logChoice)  # Intro initiation
    if (registerPath or skipToRegister) and not skipToLogin:
        execGUI(RegisterGUI, regSubmit)
        if registerValid:
            execGUI(AlertGUI, okRegister, "Register Successful", "you may now log in", "Ok")
            if skipToLogin:
                pathController()
        elif not registerValid and AlertGUI:
            execGUI(AlertGUI, tryAgainRegister, "Bad Credentials", "please choose different credentials", "Try Again")
            if skipToRegister:
                pathController()
    elif (loginPath or skipToLogin) and not skipToRegister:
        execGUI(LoginGUI, logSubmit)
        print("loginValid: ", loginValid)
        if loginValid == True:
            execGUI(AlertGUI, okLogin, "login Successful", "", "Open Asel")
            execGUI(AselMainGUI, userLookup, sendDM, refreshLite, sendCallRequest, checkIfCalled, callUsername,
                    initCallFunc, updateCamFeed, killCall, checkIfCallEnded)
        else:
            execGUI(AlertGUI, tryAgainLogin, "Login Invalid", "please check your credentials", "Try Again")
            if skipToLogin:
                pathController()


skipToLogin = True  # * temporary
pathController()  # it should be impossible for any REQ to get sent before register/login