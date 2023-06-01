import sys
import socket
import os
import inspect
import threading
from GUIcode import IntroGUI
from GUIcode import LoginGUI
from GUIcode import RegisterGUI
from GUIcode import AselMainGUI
from GUIcode import AlertGUI
from GUIcode import CallAlertGUI
import hashlib
import json
from AselClass import lastTalkedStack
import traceback
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import base64
import numpy as np
  
# define a video capture object
#setup paths
callerName = "<NAME>"
initCallGUI = False
activeChatData = ""
callPopUp = False
activeChatUser = None
activeChatUser = "ben" #* testing
recv = ""
skipToLogin = False
skipToRegister = False
registerPath = False
loginPath = False
registerSubmitPath = False
registerValid = False
loginValid = False
runAselPath = False
recentChats = lastTalkedStack(8) #a custom class stack of all recent chats with the max value being set to 8



def listenThreadTCP(): #unhanled exceptions may lead to aplication crashes
    global recentChats
    while True:            
        global callPopUp
        global callerName
        global activeChatUser
        global initCallGUI
        #print(f'[PACKET GOT]: {recv.decode()}')
        #packet =""
        packet = json.loads(recvAll(TCPclient).decode())
        try:
            if packet['registerValid'] == True:
                global registerValid
                registerValid = True
        except:
            None
        try:
            if packet['loginValid'] == True:
                global loginValid
                loginValid = True
        except:
            None
        try:

            if packet['request'] == "userLookup":
                if packet['username'] == None:
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
                callerName = packet['caller']
                callPopUp = True

            elif packet['request'] == "wasCallAccepted":
                if packet['bool']:
                    print("[CALL ACCEPTED]")
                    initCallGUI  = True
                    

                else:
                    print("[CALL DECLINED]")

        
        except:
            #traceback.print_exc()
            None    

def listenThreadUDP():
    data, address = UDPclient.recvfrom(1024)
    while True:
        print("GOT PACKET: ",data)
        pass
    
def callPopupChoice(Choice,popupObject):
    data = {"request":"callPopupChoice","acceptedCall":Choice}
    TCPclient.send(json.dumps(data).encode()) #dict -> json[str]
    popupObject.close()

def recvAll(connection):
    buffer_size = 4096  # The typical buffer size, you might need to adjust it based on your application.
    data = bytearray()
    while True:
        part = connection.recv(buffer_size)
        data.extend(part)
        if len(part) < buffer_size:
            # Either 0 or less than buffer_size bytes has been received. This means the sender has closed the connection.
            break
    return data


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




try:
    ip = 'localhost'
    global port
    global client
    port = 3080
    TCPclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPclient.connect((ip, port))
    TCPclient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #makes port available after closing
    print(f"connected on port {port}")

    # UDP client socket
    UDPclient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPclient.connect((ip, port))
    UDPclient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # makes port available after closing
    print(f"UDP socket ready on port {port}")

except:
    print("server connection failed")
    TCPclient.close()
    UDPclient.close()
try:
    threading.Thread(target=listenThreadTCP).start()  
    threading.Thread(target=listenThreadUDP).start()  
    
except:
    print(traceback.print_exc())
    print("thread initiation failed")


def regSubmit():
    global registerSubmitPath
    registerSubmitPath = True
    username = RegisterGUI.username
    passwordHash = hashlib.sha256(RegisterGUI.password.encode()).hexdigest()
    data = {"request":"register","username":username,"password":passwordHash}
    TCPclient.send((json.dumps(data)).encode()) #dict -> json[str]
    RegisterGUI.registerGlobal.close()

    
def logSubmit():
    username = LoginGUI.username
    passwordHash = hashlib.sha256(LoginGUI.password.encode()).hexdigest()
    data = {"request":"login","username":username,"password":passwordHash}
    TCPclient.send(json.dumps(data).encode()) #dict -> json[str]
    LoginGUI.loginGlobal.close()


def regChoice(): #user chose register on intro
    global registerPath
    registerPath = True
    IntroGUI.introGlobal.close()    
def logChoice(): #user chose login on intro
    global loginPath
    loginPath = True
    IntroGUI.introGlobal.close()
def okRegister():
    global skipToLogin0
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
    #run asel
    refreshChat()
    AlertGUI.alertGlobal.close()

def tryAgainLogin():
    global skipToLogin
    global skipToRegister
    skipToRegister = False
    skipToLogin = True
    AlertGUI.alertGlobal.close()

def execGUI(objectGUI,*callbacks): #function that procedurally runs a GUI module and links its paramaters
    classGUI = inspect.getmembers(objectGUI,lambda member: inspect.isclass(member))
    classGUI = classGUI[0][1]
    app = objectGUI.QtWidgets.QApplication(sys.argv)
    Asel = objectGUI.QtWidgets.QMainWindow()
    classGUI().setupUi(Asel,*callbacks)
    if objectGUI == AselMainGUI:  # This is the AselMainGUI, create an instance and keep a reference
        AselMainGUI.instance = Asel  # This stores the instance so it won't be garbage collected
        global classGUI_ins
        classGUI_ins = classGUI
    Asel.show()
    app.exec_()

def sendDM(message):
    data = {"request":"dm","target":activeChatUser,"message":message}
    if message == "" or message == None:
        data = {"request":"dm","target":activeChatUser,"message":"blankMsg"} #* testing
    TCPclient.send(json.dumps(data).encode()) #dict -> json[str]


#todo:  sqllite, encyrpted "diffie hellman",
#todo strechlist:  block 2 many requests, check both sides for illegal characters

def userLookup(customInput=None):
    if not customInput:
        #userSearch = AselMainGUI.userLookupName
        None
    else:
        userSearch=customInput
        data = {"request":"userLookup","username":userSearch}
        TCPclient.send((json.dumps(data)).encode()) #dict -> json[str]
        
def refreshLite(): #callback function that refreshes the chat with current active data
    _ = 0
    #recentChats.printStack()
    #print(recentChats.getList()[1])
    for friendBox in AselMainGUI.globalFriendBoxes:
        try:
            friendBox.setText(f"{recentChats.getList()[_]}")
        except:
            pass
        _+=1

    AselMainGUI.globalTextBox.setPlainText(activeChatData)
    

def refreshChat():
    data = {"request":"loadChat","target":activeChatUser}
    TCPclient.send((json.dumps(data)).encode()) #dict -> json[str]


def sendCallRequest():
    data = {"request":"call","targetName":activeChatUser}
    TCPclient.send((json.dumps(data)).encode()) #dict -> json[str]

def checkIfCalled():
    global callPopUp
    if callPopUp:
        AselMainGUI.AselMainGUIclass.callAlertInit(AselMainGUI.AselMainGUIclass,callPopupChoice,callerName)
        callPopUp = False


initRunOnce = False
def initCallFunc():
    global initRunOnce
    if initCallGUI:
        AselMainGUI.globalStackedWidget.setCurrentIndex(1)
        if initRunOnce == False:
            threading.Thread(target=callThreadFunc).start()  
            initRunOnce = True #TODO find where this needs to be reset for post hangup calls


def imageEncode(frameImage,compVal): # Convert the image to a base64 string
    camValidVal, buffer = cv2.imencode('.jpg', frameImage, [int(cv2.IMWRITE_JPEG_QUALITY), compVal])
    base64_image_str = str(base64.b64encode(buffer))
    return base64_image_str

def imageDecode(bytesImage): # Convert the base64 string back to an image
    img_bytes = base64.b64decode(bytesImage)
    img_arr = np.frombuffer(img_bytes, dtype=np.uint8)
    decoded_img = cv2.imdecode(img_arr, flags=cv2.IMREAD_COLOR)
    return decoded_img


            

    

#vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#camValid, frame = vid.read()
#imgBytes = imageEncode(frame)



def callThreadFunc():
    # Start video capture
    vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        camValid, frame = vid.read()
        if camValid:
            imgBytes = imageEncode(frame,70)
            UDPclient.send(imgBytes.encode())
            
        
    

#UDPclient.send()
0
#due to how pyqt5 works pythons garbage collector will automatically close windows that do not refer to themselves, thats why you can NOT-
#call PathController from a different function, a workaround to this is using "paths", which are booleans which will determine the flow
#of the menu's
def pathController():
    if not skipToLogin and not skipToRegister:
        execGUI(IntroGUI,regChoice,logChoice) #Intro initiation
    if (registerPath or skipToRegister) and not skipToLogin:
        execGUI(RegisterGUI,regSubmit)
        if registerValid == True:
            execGUI(AlertGUI,okRegister,"Register Successful","you may now log in","Ok")
            if skipToLogin:
                pathController()
        elif registerValid == False and AlertGUI:
            execGUI(AlertGUI,tryAgainRegister,"Bad Credentials","please choose different credentials","Try Again")
            if skipToRegister:
                pathController()
    elif (loginPath or skipToLogin) and not skipToRegister: 
        execGUI(LoginGUI,logSubmit)
        print("loginValid: ",loginValid)
        if loginValid == True:
            execGUI(AlertGUI,okLogin,"login Successful","","Open Asel")
            execGUI(AselMainGUI,userLookup,sendDM,refreshLite,sendCallRequest,checkIfCalled,callerName,initCallFunc)
        else:
            execGUI(AlertGUI,tryAgainLogin,"Login Invalid","please check your credentials","Try Again")
            if skipToLogin:
                pathController()


skipToLogin = True #* temporary
pathController() #it should be impossible for any REQ to get sent before register/login




