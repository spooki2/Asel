import threading
import socket
import json
import os
import traceback
import time

# setup variables


threadCount = threading.active_count() - 1  # -1 because main doesn't count
activeConnections = 0
regID = 0
with open('DataBase\\UserDataBase.txt') as DB:
    DBlines = DB.readlines()
    for DBline in DBlines:
        regID += 1
# regID is the ID of each users register line, it cannot be changed unlike names.
# the function above makes regID the last line available
ip = '0.0.0.0'
port = 4000

while True:
    try:
        TCPserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCPserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # makes port available after closing
        TCPserver.bind((ip, port))
        TCPserver.listen()

        UDPserverWebcam = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDPserverWebcam.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # makes port available after closing
        UDPserverWebcam.bind((ip, (port + 1)))

        UDPserverMic = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDPserverMic.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # makes port available after closing
        UDPserverMic.bind((ip, (port + 2)))
        print(f"[SERVER ONLINE] [PORT {port}]")
        break
    except WindowsError:
        print("[Server Setup Failed]")
        print("retrying...\n")
        time.sleep(3)


def isValidJson(jsonString):  # checks if string is valid json
    try:
        json.loads(jsonString)
        return True
    except ValueError:
        return False


def formatUserInfo(userInfo):
    return {"id": regID, "username": userInfo['username'], "password": userInfo['password']}
    # func returns id, name and password as DICT


def databaseSave(userInfo):  # dict storing on database
    with open('DataBase\\UserDataBase.txt', "a+") as database:
        global regID
        regID += 1  # new ID for new user
        database.write(f"\n{json.dumps(formatUserInfo(userInfo))}")  # saves stripped json[str] in database


def databaseCheck(userInfo, nameOnly=False):  ##login validation
    with open('DataBase\\UserDataBase.txt') as database:
        lines = database.readlines()
    if not nameOnly:
        LoginValid = False
        formatedUserInfo = formatUserInfo(userInfo)
        for line in lines:
            nameDB = json.loads(line)["username"]
            passwordDB = json.loads(line)["password"]
            if nameDB == formatedUserInfo["username"] and passwordDB == formatedUserInfo["password"]:
                LoginValid = True
        return LoginValid
    if nameOnly:
        for line in lines:
            nameDB = json.loads(line)["username"]
            if nameDB == userInfo["username"]:
                return nameDB
    return None


def sortStrings(s1, s2):  # sorts strings alphabetically
    if s1 < s2:
        return s1, s2
    else:
        return [s2, s1]


def countLines(filePath):
    try:
        with open(filePath, 'r') as file:
            lines = file.readlines()
            lineCount = len(lines)
            return lineCount + 1
    except FileNotFoundError:
        print(f"File not found: {filePath}")
        return None


def dmServerManager(senderName, targetName, message, onlyLoad=False):
    # dmServerManager (direct message server manager) is a function that routes messages and manages chats in Asel,
    # here is the logic:
    orderedNameFirst = sortStrings(senderName, targetName)[0]
    orderedNameSecond = sortStrings(senderName, targetName)[1]
    trueTitle = f"{orderedNameFirst},{orderedNameSecond}"
    path = f"DataBase\\\ChatDataBase\\\{trueTitle}.txt"
    chatTitles = os.listdir("DataBase\\ChatDataBase")
    titleFound = False
    for title in chatTitles:
        if title == f"{trueTitle}.txt":
            titleFound = True
    if not titleFound:
        with open(path, "a+") as newChat:
            adminMsg = f"This is the beginning of {orderedNameFirst}'s chat with {orderedNameSecond}"
            newChat.write(json.dumps({"sender": "server", "message": adminMsg}))

        print("[CREATED NEW CHAT TXT]")
    # if user01 sends user02 a message and they never talked before: [check user01|user02 & user02|user01]
    # make a new empty file to store their chat in the database, call it: "user01,user02" (alphabetically ordered)
    if not onlyLoad:
        with open(path, "a+") as chatDB:
            data = {"sender": senderName, "message": message}
            if countLines(path) != 1:
                chatDB.write("\n")
            chatDB.write(json.dumps(data))

        # update the txt file with [sender:"_",message:"_"]
    with open(path, "r") as chatDB:
        read = chatDB.read()
        S_dataChatDB = {"request": "loadChat", "from": targetName, "data": read}
        T_dataChatDB = {"request": "loadChat", "from": senderName, "data": read}

        try:  # the user may be online, and therefore cannot receive the packet, no matter, he will receive it when
            # he logs back in.
            getSocketByName(senderName).send(json.dumps(S_dataChatDB).encode())
        except:
            traceback.print_exc()
            pass
        try:
            getSocketByName(targetName).send(json.dumps(T_dataChatDB).encode())
        except:
            pass
        # send both users {request:"updateChat","users":{<user1 socket>,<user2 socket>},<user01|user02 file>"}


callChoiceEvent = threading.Event()
killCallEvent = threading.Event()
callChoiceEvent.choice = False
killCallEvent.choice = False


def callManager(callerName, targetName):  # this function manages calls between users, hang ups and all other
    global callChoiceEvent
    global killCallEvent
    callChoiceEvent = threading.Event()
    killCallEvent = threading.Event()
    callChoiceEvent.choice = False
    killCallEvent.choice = False
    targetSocket = getSocketByName(targetName)
    callerSocket = getSocketByName(callerName)
    # send target call popup request
    targetSocket.send(json.dumps({'request': 'callPopup', 'caller': callerName}).encode())
    callChoiceEvent.wait()  # waits for accept or decline
    if callChoiceEvent.choice:  # let both know if call accepted or declined
        data = {'request': 'wasCallAccepted', 'bool': True}
        print("[CALL ACCEPTED] routing call..")
        threading.Thread(target=callThread, args=(callerName, targetName)).start()
    else:
        data = {'request': 'wasCallAccepted', 'bool': False}
        print("[CALL DECLINED]")
    data = json.dumps(data)
    targetSocket.send(data.encode())
    callerSocket.send(data.encode())


def callThread(callerName, targetName):
    print(f"[Call Started Between <{callerName}> and <{targetName}>]")
    callAlive = True
    while callAlive:
        if killCallEvent.choice:
            callAlive = False
        callerCamAddr = nameToCamAddr[callerName]
        targetCamAddr = nameToCamAddr[targetName]
        callerMicAddr = nameToMicAddr[callerName]
        targetMicAddr = nameToMicAddr[targetName]

        # print(f"target: {callerMicAddr}")
        # print(f"list: {addrToMicData}")
        # print("daj: ",addrToMicData[callerMicAddr])
        # print("")
        try:
            UDPserverMic.sendto(addrToMicData[callerMicAddr], targetMicAddr)
        except:
            traceback.print_exc()
            pass
        try:
            UDPserverMic.sendto(addrToMicData[targetMicAddr], callerMicAddr)
        except:
            traceback.print_exc()
            pass
        try:
            UDPserverWebcam.sendto(addrToWebcamData[callerCamAddr], targetCamAddr)
        except:
            pass
        try:
            UDPserverWebcam.sendto(addrToWebcamData[targetCamAddr], callerCamAddr)
        except:
            pass
    data = json.dumps({"request": "callEnded"})
    getSocketByName(callerName).send(data.encode())
    getSocketByName(targetName).send(data.encode())
    print("[Call Ended]")


addrToWebcamData = {}
addrToMicData = {}  # they both track data corelated with addresss

nameToCamAddr = {}
nameToMicAddr = {}  # they both track the ip and the udp port of each name

socketNames = {}  # declartion, dict maps usernames to sockets {username:socket}
addressNames = {}


def TCPhandleClient(clientSocket, clientAddress):
    ConnectionDead = False
    global activeConnections
    global socketNames
    global nameToCamAddr
    global nameToMicAddr
    global addressNames
    activeConnections += 1
    print(f"[TCP CONNECTION STARTED {clientAddress}] [{activeConnections} Total]")
    while not ConnectionDead:  # runs as long as user connected
        try:
            recv = clientSocket.recv(1024)
            packet = recv.decode()
            if isValidJson(packet):  # json format validation
                userInfo = json.loads(packet)
                # userInfo is DICT
                if userInfo['request'] == "register":
                    frmtUserInfo = formatUserInfo(userInfo)
                    if frmtUserInfo['username'] == "" or frmtUserInfo['password'] == "":
                        clientSocket.send(json.dumps({"registerValid": False}).encode())
                        print("[REGISTER]: invalid")

                    elif not databaseCheck(userInfo):
                        databaseSave(userInfo)
                        clientSocket.send(json.dumps({"registerValid": True}).encode())
                        print("[REGISTER]: valid")
                    else:
                        clientSocket.send(json.dumps({"registerValid": False}).encode())
                        print("[REGISTER]: invalid")

                elif userInfo['request'] == "login":
                    if databaseCheck(userInfo):
                        clientSocket.send(json.dumps({"loginValid": True}).encode())
                        socketNames[userInfo['username']] = clientSocket
                        addressNames[userInfo['username']] = clientAddress
                        clientName = userInfo['username']
                    else:
                        clientSocket.send(json.dumps({"loginValid": False}).encode())
                        print("[SENT CLIENT]: invalid login")
                elif userInfo['request'] == "userLookup":
                    # clientSocket.send(json.dumps({"userLookup":}))
                    userFound = databaseCheck(userInfo, True)
                    clientSocket.send(json.dumps({"request": "userLookup", "username": userFound}).encode())
                elif userInfo['request'] == "dm":
                    dmServerManager(clientName, userInfo["target"], userInfo["message"])
                elif userInfo['request'] == "loadChat":
                    dmServerManager(clientName, userInfo["target"], "", True)

                elif userInfo['request'] == "call":
                    nameToCamAddr[clientName] = (clientAddress[0], userInfo['UDPcamPort'])
                    nameToMicAddr[clientName] = (clientAddress[0], userInfo['UDPmicPort'])
                    threading.Thread(target=callManager, args=(clientName, userInfo['targetName'])).start()

                elif userInfo['request'] == "callPopupChoice":
                    print("[CALL POPUP CHOICE] ", userInfo['acceptedCall'])
                    nameToCamAddr[clientName] = (clientAddress[0], userInfo['UDPcamPort'])
                    nameToMicAddr[clientName] = (clientAddress[0], userInfo['UDPmicPort'])

                    if userInfo['acceptedCall']:
                        callChoiceEvent.choice = True
                    callChoiceEvent.set()
                elif userInfo['request'] == "killCall":
                    killCallEvent.choice = True
                    killCallEvent.set()
                elif userInfo['request'] == "relay":
                    jsonUF = json.dumps(userInfo)
                    jsonUF = jsonUF.replace('"request": "relay", ', '')
                    jsonUF = jsonUF.replace('Relay', '')
                    targetName = userInfo['target']
                    jsonUF = jsonUF.replace(f'"target": "{targetName}", ', '')
                    print("jsonUF: ", jsonUF)
                    getSocketByName(targetName).send(jsonUF.encode())

            else:
                print(f"[GOT INVALID PACKET]: {packet}")
                raise Exception("[JSON RECEIVED IS NOT VALID]")

        except:
            ConnectionDead = True
            activeConnections -= 1
            # traceback.print_exc() #prints the exception
            print("")
            print(f"[TCP CONNECTION TERMINATED {clientAddress}] [{activeConnections} Total]")


def getSocketByName(name):
    if name in socketNames:
        socketFound = socketNames[name]
        return socketFound
    else:
        print("[getSocketByName FAILED]")
        print(F'looked for [{name}] in [{socketNames}]')


def UDPcamThread():
    while True:
        webcamData, webcamAddr = UDPserverWebcam.recvfrom(90000)
        addrToWebcamData[webcamAddr] = webcamData


def UDPmicThread():
    while True:
        try:
            micData, micAddr = UDPserverMic.recvfrom(2048*2)  # stuck on
            addrToMicData[micAddr] = micData
        except:
            print("error in thread")
            traceback.print_exc()


threading.Thread(target=UDPcamThread).start()
threading.Thread(target=UDPmicThread).start()

while True:
    TCPclientSocket, TCPclientAddress = TCPserver.accept()
    # while true is frozen, waiting for connection
    threading.Thread(target=TCPhandleClient, args=(TCPclientSocket, TCPclientAddress)).start()
