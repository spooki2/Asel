import json
import socket
import threading
import sqlite3
import hashlib
from AselClass import hellmanClass

# setup variables


threadCount = threading.active_count() - 1  # -1 because main doesn't count
activeConnections = 0
noUsersConnected = True

# regID is the ID of each users register line, it cannot be changed unlike names.
# the function above makes regID the last line available
ip = '0.0.0.0'
port = 4012
userDB = 'UserDataBase.db'
chatDB = 'chatDataBase.db'

userConn = sqlite3.connect(userDB, check_same_thread=False)
userPointer = userConn.cursor()

chatConn = sqlite3.connect(chatDB)
chatPointer = chatConn.cursor()

userPointer.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER, username TEXT, password TEXT)''')

userPointer.execute("SELECT COUNT(*) FROM users")
regID = userPointer.fetchone()[0]


def closeSQLall():
    global userConn
    global userPointer
    global chatConn
    global chatPointer
    userPointer.close()
    userConn.close()
    chatPointer.close()
    chatConn.close()


def openSQLall():
    global userConn
    global userPointer
    global chatConn
    global chatPointer
    userConn = sqlite3.connect(userDB, check_same_thread=False)
    userPointer = userConn.cursor()
    chatConn = sqlite3.connect(chatDB, check_same_thread=False)
    chatPointer = chatConn.cursor()


closeSQLall()

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


def databaseSave(userInfo):  # dict storing on dautabase
    global regID
    regID += 1  # new ID for new user
    userPointer.execute("INSERT INTO users (id, username, password) VALUES (?,?, ?)",
                        (regID, userInfo['username'], userInfo['password']))
    userConn.commit()


def databaseCheck(userInfo, nameOnly=False):  ##login validation
    userPointer.execute("SELECT username, password FROM users WHERE username=?", (userInfo['username'],))
    user = userPointer.fetchone()
    if user:
        if nameOnly:
            return user[0]
        else:
            return user[0] == userInfo['username'] and user[1] == userInfo['password']
    return None


def sortStrings(s1, s2):  # sorts strings alphabetically
    if s1 < s2:
        return s1, s2
    else:
        return [s2, s1]


def dmServerManager(senderName, targetName, message, onlyLoad=False):
    orderedNameFirst, orderedNameSecond = sortStrings(senderName, targetName)
    trueTitle = f"{orderedNameFirst},{orderedNameSecond}"

    # Create table if it does not exist

    chatPointer.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{trueTitle}'")
    tableExists = chatPointer.fetchone()

    if tableExists is None:
        chatPointer.execute(f"CREATE TABLE IF NOT EXISTS '{trueTitle}' (sender TEXT, message TEXT)")
        adminMsg = f"This is the beginning of {orderedNameFirst}'s chat with {orderedNameSecond}"
        chatPointer.execute(f"INSERT INTO '{trueTitle}' (sender, message) VALUES (?, ?)", ("server", adminMsg))
        chatConn.commit()
        print("[CREATED NEW CHAT TABLE]")

    if not onlyLoad:
        chatPointer.execute(f"INSERT INTO '{trueTitle}' (sender, message) VALUES (?, ?)", (senderName, message))
        chatConn.commit()

    rows = chatPointer.execute(f"SELECT * FROM '{trueTitle}'").fetchall()
    appendData = ""
    for row in rows:
        # print(f"{row[0]}: {row[1]}")
        # line = {row[0]: row[1]}
        rowSplit = '{' + f'"sender":"{row[0]}","message":"{row[1]}"' + '}'

        appendData += rowSplit + "\n"

    S_dataChatDB = {"request": "loadChat", "from": targetName, "data": appendData}
    T_dataChatDB = {"request": "loadChat", "from": senderName, "data": appendData}

    try:
        S_dataChatDB = addrToHellman[nameToTCPaddr[senderName]].encrypt(json.dumps(S_dataChatDB))
        getSocketByName(senderName).send(S_dataChatDB.encode())
    except:
        pass
    try:
        T_dataChatDB = addrToHellman[nameToTCPaddr[targetName]].encrypt(json.dumps(T_dataChatDB))
        getSocketByName(targetName).send(T_dataChatDB.encode())
    except:
        pass


callChoiceEvent = threading.Event()
killCallEvent = threading.Event()
callChoiceEvent.choice = False
killCallEvent.choice = False

callChoiceEvent = threading.Event()
killCallEvent = threading.Event()
callChoiceEvent.choice = False
killCallEvent.choice = False


def callManager(callerName, targetName):  # this function manages calls between users, hang ups and all other
    global callChoiceEvent
    global killCallEvent
    callChoiceEvent = threading.Event()
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
    global addrToMicData
    global addrTocamData
    print(f"[Call Started Between <{callerName}> and <{targetName}>]")
    callAlive = True
    while callAlive:
        if killCallEvent.choice:
            callAlive = False

        callerCamAddr = nameToCamAddr[callerName]
        targetCamAddr = nameToCamAddr[targetName]
        callerMicAddr = nameToMicAddr[callerName]
        targetMicAddr = nameToMicAddr[targetName]

        try:
            UDPserverMic.sendto(addrToMicData[callerMicAddr], targetMicAddr)
        except:
            pass
        try:
            UDPserverMic.sendto(addrToMicData[targetMicAddr], callerMicAddr)
        except:
            pass
        try:
            UDPserverWebcam.sendto(addrTocamData[callerCamAddr], targetCamAddr)
        except:
            pass
        try:
            UDPserverWebcam.sendto(addrTocamData[targetCamAddr], callerCamAddr)
        except:
            pass
    data = json.dumps({"request": "callEnded"})
    getSocketByName(callerName).send(data.encode())
    getSocketByName(targetName).send(data.encode())
    print("[Call Ended]")

    addrTocamData = {}
    addrToMicData = {}  # empties all data upon hanging up


addrTocamData = {}
addrToMicData = {}  # they both track data corelated with addresss

nameToCamAddr = {}
nameToMicAddr = {}  # they both track the ip and the udp port of each name

nameToTCPaddr = {}

addrToHellman = {}  # maps class to addrs
addrToPrivateKey = {}
socketNames = {}
# generates a temporary private key [WITHOUT SHARING] per each session and correlates it to the address-
# of a connected client.

def TCPhandleClient(clientSocket, clientAddress):
    ConnectionDead = False
    global activeConnections
    global socketNames
    global nameToCamAddr
    global nameToMicAddr
    global noUsersConnected
    global nameToTCPaddr
    global addrToHellman
    activeConnections += 1
    print(f"[TCP CONNECTION STARTED {clientAddress}] [{activeConnections} Total]")
    while not ConnectionDead:  # runs as long as user connected
        try:
            if noUsersConnected:
                print("[Opening Databases..]")
                openSQLall()
                noUsersConnected = False
            packetRaw = clientSocket.recv(1024)
            packet = packetRaw.decode()
            if isValidJson(packet):  # json format validation
                userInfo = json.loads(packet)
                # userInfo is DICT
                if userInfo['request'] == "exchangeKeys":
                    addrToHellman[clientAddress] = hellmanClass(userInfo['key'])
                    clientSocket.send(json.dumps(
                        {"request": "exchangeKeys", "key": addrToHellman[clientAddress].getMyPublic()}).encode())
                    addrToHellman[clientAddress].generateSharedKey()
                elif userInfo['request'] == "register":
                    userInfo['username'] = addrToHellman[clientAddress].decrypt(userInfo['username'])
                    userInfo['password'] = addrToHellman[clientAddress].decrypt(userInfo['password'])
                    frmtUserInfo = formatUserInfo(userInfo)
                    if frmtUserInfo['username'] == "" or frmtUserInfo['password'] == hashlib.sha256(
                            "".encode()).hexdigest():
                        clientSocket.send(json.dumps({"request": "registerStatus", "registerValid": False}).encode())
                        print("[REGISTER]: invalid")

                    elif not databaseCheck(userInfo):
                        databaseSave(userInfo)
                        clientSocket.send(json.dumps({"request": "registerStatus", "registerValid": True}).encode())
                        print("[REGISTER]: valid")
                    else:
                        clientSocket.send(json.dumps({"request": "registerStatus", "registerValid": False}).encode())
                        print("[REGISTER]: invalid")

                elif userInfo['request'] == "login":
                    userInfo['username'] = addrToHellman[clientAddress].decrypt(userInfo['username'])
                    userInfo['password'] = addrToHellman[clientAddress].decrypt(userInfo['password'])

                    if databaseCheck(userInfo):
                        clientSocket.send(json.dumps({"request": "loginStatus", "loginValid": True}).encode())
                        socketNames[userInfo['username']] = clientSocket
                        nameToTCPaddr[userInfo['username']] = clientAddress
                        clientName = userInfo['username']
                    else:
                        clientSocket.send(json.dumps({"request": "loginStatus", "loginValid": False}).encode())
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
                    getSocketByName(targetName).send(jsonUF.encode())

            else:
                print(f"[GOT INVALID PACKET]: {packet}")
                raise Exception("[JSON RECEIVED IS NOT VALID]")

        except:
            ConnectionDead = True
            activeConnections -= 1
            print("")
            print(f"[TCP CONNECTION TERMINATED {clientAddress}] [{activeConnections} Total]")
            if activeConnections == 0:
                noUsersConnected = True
                print(f"[SAVING MEMORY, CLOSING DATABASE]")
                closeSQLall()


def getSocketByName(name):
    if name in socketNames:
        socketFound = socketNames[name]
        return socketFound


def UDPcamThread():
    while True:
        try:
            webcamData, webcamAddr = UDPserverWebcam.recvfrom(50000)
            addrTocamData[webcamAddr] = webcamData
        except:
            pass


def UDPmicThread():
    while True:
        try:
            micData, micAddr = UDPserverMic.recvfrom(50000)
            addrToMicData[micAddr] = micData
        except:
            pass


threading.Thread(target=UDPcamThread).start()
threading.Thread(target=UDPmicThread).start()

while True:
    TCPclientSocket, TCPclientAddress = TCPserver.accept()
    # while true is frozen, waiting for connection
    threading.Thread(target=TCPhandleClient, args=(TCPclientSocket, TCPclientAddress)).start()
