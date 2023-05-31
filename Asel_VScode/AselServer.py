import threading
import socket
import json
import os
import traceback
#setup variables


threadCount = threading.active_count()-1 # -1 because main doesn't count
activeConnections = 0
regID = 0
with open('DataBase\\UserDataBase.txt') as database:
    lines = database.readlines()
    for line in lines:
        regID+=1
#regID is the ID of each users register line, it cannot be changed unlike names.
#the function above makes regID the last line available
ip = 'localhost'
port = 3000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #makes port available after closing
server.bind((ip,port))
server.listen()
print(f"[SERVER ONLINE] [PORT {port}]")



def isValidJson(jsonString): #checks if string is valid json
    try:
        json.loads(jsonString)
        return True
    except ValueError as e:
        return False

def formatUserInfo(userInfo):
    return {"id":regID,"username":userInfo['username'],"password":userInfo['password']}
    #func returns id, name and password as DICT

def databaseSave(userInfo): #dict storing on database
    with open('DataBase\\UserDataBase.txt', "a+") as database:
        global regID
        regID+=1 #new ID for new user
        database.write(f"\n{json.dumps(formatUserInfo(userInfo))}") #saves stripped json[str] in database

def databaseCheck(userInfo,nameOnly=False): ##login validation
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

def sortStrings(s1, s2): #sorts strings alphabetically
    if s1 < s2:
        return s1, s2
    else:
        return [s2, s1]

def countLines(filePath):
    try:
        with open(filePath, 'r') as file:
            lines = file.readlines()
            lineCount = len(lines)
            return lineCount+1
    except FileNotFoundError:
        print(f"File not found: {filePath}")
        return None


def dmServerManager(senderName,targetName,message,onlyLoad=False):
    #dmServerManager (direct message server manager) is a function that routes messages and manages chats in Asel, here is the logic:
    orderedNameFirst = sortStrings(senderName,targetName)[0]
    orderedNameSecond = sortStrings(senderName,targetName)[1]
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
            newChat.write(json.dumps({"sender":"server","message":adminMsg}))

        print("[CREATED NEW CHAT TXT]")
    #if user01 sends user02 a message and they never talked before: [check user01|user02 & user02|user01]
    #make a new empty file to store their chat in the database, call it: "user01,user02" (alphabetically ordered)
    if not onlyLoad:
        with open(path, "a+") as chatDB:
            data = {"sender":senderName,"message":message}
            if countLines(path) != 1:
                chatDB.write("\n")
            chatDB.write(json.dumps(data))

        #update the txt file with [sender:"_",message:"_"]
    with open(path, "r") as chatDB:
        read = chatDB.read()
        S_dataChatDB = {"request":"loadChat","from":targetName,"data":read}
        T_dataChatDB = {"request":"loadChat","from":senderName,"data":read}

        
        try: #the user may be online, and therefore cannot receive the packet, no matter, he will receive it when he logs back in.
            getSocketByName(senderName).send(json.dumps(S_dataChatDB).encode())
        except:
            None
        try:
            getSocketByName(targetName).send(json.dumps(T_dataChatDB).encode())
        except:
            None
        #send both users {request:"updateChat","users":{<user1 socket>,<user2 socket>},<user01|user02 file>"}


def callManager(callerName,targetName): #this function manages calls between users, hang ups and all other
    global callChoiceEvent
    callChoiceEvent = threading.Event()
    callChoiceEvent.choice = False

    targetSocket = getSocketByName(targetName)
    callerSocket = getSocketByName(callerName)
    
    #send target call popup request
    targetSocket.send(json.dumps({'request':'callPopup','caller':callerName}).encode())
    callChoiceEvent.wait() #waits for accept or decline
    if callChoiceEvent.choice: #let both know if call accepted or declined
        data = {'request':'wasCallAccepted','bool':True}
        print("[CALL ACCEPTED] routing call..")
    else:
        data = {'request':'wasCallAccepted','bool':False}
        print("[CALL DECLINED]")
    data = json.dumps(data)
    targetSocket.send(data.encode())
    callerSocket.send(data.encode())
    print("data: ", data)
    
    #logic:
    #if a user is calling, send the target a popup where they can hang up or accept
    #if they accept, send both the request to init call GUI and start data transfer on UDP
    




socketNames = {} #declartion, dict maps usernames to sockets {username:socket}
def handleClient(clientSocket, clientAddress):
    ConnectionDead = False
    global activeConnections
    global socketNames
    activeConnections+=1
    print(f"[CONNECTION STARTED {clientAddress}] [{activeConnections} Total]")
    while not ConnectionDead: #runs as long as user connected
        recv = clientSocket.recv(1024)
        packet = recv.decode()
        try:
            if isValidJson(packet): #json format validation
                userInfo = json.loads(packet)
                #userInfo is DICT
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
                        clientName = userInfo['username']
                    else:
                        clientSocket.send(json.dumps({"loginValid": False}).encode()) 
                        print("[SENT CLIENT]: invalid login")
                elif userInfo['request'] == "userLookup":
                    #clientSocket.send(json.dumps({"userLookup":}))
                    userFound = databaseCheck(userInfo,True)
                    clientSocket.send(json.dumps({"request":"userLookup","username":userFound}).encode()) 
                elif userInfo['request'] == "dm":
                    dmServerManager(clientName,userInfo["target"],userInfo["message"])
                elif userInfo['request'] == "loadChat":
                    dmServerManager(clientName,userInfo["target"],"",True)

                elif userInfo['request'] == "call":
                    callThread = threading.Thread(target=callManager, args=(clientName, userInfo['targetName']))
                    callThread.start()
                    #! what is lambda?
                
                elif userInfo['request'] == "callPopupChoice":
                    global callChoiceEvent
                    print("[CALL POPUP CHOICE] ",userInfo['acceptedCall'])
                    if userInfo['acceptedCall'] == True:
                        callChoiceEvent.choice = True
                    callChoiceEvent.set()
                    
                    
            else:
                print(f"[GOT INVALID PACKET]: {packet}")
                raise Exception("[JSON RECEIVED IS NOT VALID]")
        
        except Exception as e:
            ConnectionDead = True
            activeConnections-=1
            traceback.print_exc() #prints the exception
            print("")
            print(f"[CONNECTION TERMINATED {clientAddress}] [{activeConnections} Total]")


def getSocketByName(name):
    if name in socketNames:
        socket = socketNames[name]
        return socket



while True:
    clientSocket, clientAddress = server.accept()
    #while true is frozen, waiting for connection
    thread = threading.Thread(target=handleClient, args=(clientSocket, clientAddress))
    thread.start()
    

