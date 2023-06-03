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
port = 3080
TCPserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #makes port available after closing
TCPserver.bind((ip,port))
TCPserver.listen()


UDPserver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #makes port available after closing
UDPserver.bind((ip, port))

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
        threading.Thread(target=callThread,args=(callerName,targetName)).start()
        
    else:
        data = {'request':'wasCallAccepted','bool':False}
        print("[CALL DECLINED]")
    data = json.dumps(data)
    targetSocket.send(data.encode())
    callerSocket.send(data.encode())
    

def callThread(callerName,targetName): #! for next time make it so it sends indiv webcam data
    while True: #TODO KILL OFF AFTER CALL

        UDPcallerAddress = UDPnameToAddr[callerName]
        UDPtargetAddress = UDPnameToAddr[targetName]

        
        try:
            UDPserver.sendto(UDPaddrToData[UDPcallerAddress],UDPtargetAddress)
            #print("UDPaddrToData PROBLem: ",UDPaddrToData[UDPcallerAddress])
        except:
            #print("exep1")
            #traceback.print_exc()
            #quit()
            pass
        try:
            UDPserver.sendto(UDPaddrToData[UDPtargetAddress],UDPcallerAddress)
            #print(UDPtargetAddress)
        except:
            #print("exep2")
            pass



    #logic:
    #if a user is calling, send the target a popup where they can hang up or accept
    #if they accept, send both the request to init call GUI and start data transfer on UDP
UDPaddrToData = {} #tracks data corelated with addresss
UDPnameToAddr = {} #tracks the ip and the udp port of each name
#def UDPhandleClient(data, UDPaddress): 

    #UDPaddrToData[UDPaddress] = data
    #UDPportToName[UDPaddress] = data
    #UDPserver.sendto(data, UDPaddress)
    
    #TODO make it so that data gets cross sent between users

socketNames = {} #declartion, dict maps usernames to sockets {username:socket}
addressNames = {}
def TCPhandleClient(clientSocket, clientAddress):
    ConnectionDead = False
    global activeConnections
    global socketNames
    global UDPnameToAddr
    global addressNames
    activeConnections+=1
    print(f"[TCP CONNECTION STARTED {clientAddress}] [{activeConnections} Total]")
    while not ConnectionDead: #runs as long as user connected
        try:
            recv = clientSocket.recv(1024)
            packet = recv.decode()
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
                        addressNames[userInfo['username']] = clientAddress
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
                    UDPnameToAddr[clientName] = (clientAddress[0],userInfo['UDPport'])
                    callThread = threading.Thread(target=callManager, args=(clientName, userInfo['targetName']))
                    callThread.start()
                
                elif userInfo['request'] == "callPopupChoice":
                    global callChoiceEvent
                    print("[CALL POPUP CHOICE] ",userInfo['acceptedCall'])
                    UDPnameToAddr[clientName] = (clientAddress[0],userInfo['UDPport'])
                    if userInfo['acceptedCall'] == True:
                        callChoiceEvent.choice = True
                    callChoiceEvent.set()

                elif userInfo['request'] == "relay":
                    jsonUF = json.dumps(userInfo)
                    jsonUF = jsonUF.replace('"request": "relay", ','')
                    jsonUF = jsonUF.replace('Relay','')
                    
                    clientSocket.send(jsonUF.encode())
                    
                
            else: 
                print(f"[GOT INVALID PACKET]: {packet}")
                raise Exception("[JSON RECEIVED IS NOT VALID]")

        except Exception as e:
            ConnectionDead = True
            activeConnections-=1
            #traceback.print_exc() #prints the exception
            print("")
            print(f"[TCP CONNECTION TERMINATED {clientAddress}] [{activeConnections} Total]")

def getSocketByName(name):
    if name in socketNames:
        socket = socketNames[name]
        return socket



def UDPthread():
    while True:
        data, address = UDPserver.recvfrom(90000)
        UDPaddrToData[address] = data
        #print(f"UDPaddrSent: {UDPnameToAddr}")
        #print(f"UDPaddrLogd: {UDPaddrToData}")
        #threading.Thread(target=UDPhandleClient, args=(data, address)).start()
        #print("active: ",threading.active_count())

threading.Thread(target=UDPthread).start()


while True:
    TCPclientSocket, TCPclientAddress = TCPserver.accept()
    #while true is frozen, waiting for connection
    threading.Thread(target=TCPhandleClient, args=(TCPclientSocket, TCPclientAddress)).start()  
    

