import socket
import random
import traceback


# functions for encryption and decryption with a key, i invented these functions from scratch-
# but im sure someone has alerady thought of this.
# logic:
# turn split word to [w,o,r,d]
# split key to [5343,4321,4309,2011] (1 mini key per each letter of word)
# turn them both to int
# for encrypt, add, for decrypt subtract
# back to STR and return
def prepareKey(data, key):  # prepares the key value so that it can be seperated to equal segments
    keyStr = str(key)
    dataStr = str(data)
    keyLen = len(keyStr)
    dataLen = len(dataStr)
    modKD = keyLen % dataLen

    # makes the key repeat its start till it has a % value of 0
    i = 0
    while modKD != 0:
        keyStr += keyStr[i]
        modKD = len(keyStr) % len(dataStr)
        i += 1
    keyLen = len(keyStr)
    dataLen = len(dataStr)

    # seperates the key to  equally long data character lists
    # example:
    # does : ['12', '34', '56', '78', '90', '12']
    # for hello ('h', 'e', 'l', 'l', 'o', 'o')
    keyList = []
    chunkSize = int(keyLen / dataLen)
    run = 0
    while run != keyLen:
        keyChunk = keyStr[run:run + chunkSize]
        keyList.append(keyChunk)
        run += chunkSize

    # reformat keylist with its unicode count per letter:
    ordKeyList = []
    for keyChunk in keyList:
        ordChunk = 0
        for char in keyChunk:
            ordChunk += ord(char)
        ordKeyList.append(ordChunk)
    return ordKeyList


def aselEncrypt(data, key):
    keyStr = str(key)
    dataStr = str(data)

    ordKeyList = prepareKey(dataStr, keyStr)
    # per each letter (member of dataLst), turn to number [ord()] and add (encryption)
    combinedList = []
    for char, val in zip(dataStr, ordKeyList):
        combinedList.append(ord(char) + val)

    # back to text (might not render chars on python console?)
    encryptedData = ""
    for val in combinedList:
        encryptedData += chr(val)
    return encryptedData


def aselDecrypt(data, key):
    keyStr = str(key)
    dataStr = str(data)

    ordKeyList = prepareKey(dataStr, keyStr)
    # per each letter (member of dataLst), turn to number [ord()] and subtract (decryption)
    combinedList = []
    for char, val in zip(dataStr, ordKeyList):
        combinedList.append(ord(char) - val)

    # back to text (might not render chars on python console?)
    encryptedData = ""
    for val in combinedList:
        encryptedData += chr(val)
    return encryptedData


# Generate a private key for use in the exchange.

aselModulus = 168781676250124572306428759106299747071460138689050751360323236565859422171436169633170447980317056837535001146509347031708310110061445304036533855635906506893597067521442258372892757697663611489318746314751913850098783334634063879113135870782586013625596717246544788855237845180595991024651559707553487529040489
# large modulus number, used in all asel applications in all runs
aselBase = 5  # small number used as a base for computations,
# these do not cause a vulnerability


randomNumMax = aselModulus - random.randint(100, 100000)
randomNumMin = random.randint(100, 100000)


# this function gets a key and compresses it into a shorter, yet equally random value
# the math is hard to explain in comments but it matches the key length to the string length:

class hellmanClass:  # Diffie Hellman encryption/decryption built into a class, specifically for Asel
    def __init__(self, peerPublicKey):
        self.sharedKey = None
        self.privateKey = random.randint(randomNumMin, randomNumMax)
        self.publicKey = pow(aselBase, self.privateKey, aselModulus)
        self.peerPublicKey = peerPublicKey

    def setPeerPublic(self, peerPublic):
        self.peerPublicKey = peerPublic

    def generateSharedKey(self):
        if self.peerPublicKey is not None:
            self.sharedKey = pow(self.peerPublicKey, self.privateKey, aselModulus)
        else:
            pass
            raise ValueError("Peer's public key is not set.")

    def debug(self):
        print(" public: ", self.publicKey)
        print("private: ", self.privateKey)
        print("   peer: ", self.peerPublicKey)
        print("modulus: ", aselModulus)

    def getMyShared(self):
        return self.sharedKey

    def encrypt(self, data):
        return aselEncrypt(data, self.sharedKey)

    def decrypt(self, data):
        return aselDecrypt(data, self.sharedKey)

    def getMyPublic(self):
        return self.publicKey


class lastTalkedStack:
    def __init__(self, maxSize=None):
        self.items = []
        self.maxSize = None
        if maxSize:
            self.maxSize = maxSize - 1

    def pop(self):
        return self.items.pop()

    def isEmpty(self):  # boolean return
        return len(self.items) == 0

    def top(self):
        temp = self.items.pop()
        self.items.append(temp)
        return temp

    def popBottom(self):
        temp = self.items[::-1][len(self.items) - 1]
        self.items = self.items[::-1]
        self.items.pop()
        self.items = self.items[::-1]
        return temp

    def topBottom(self):
        temp = self.items[::-1][len(self.items) - 1]
        return temp

    def getList(self):
        return self.items[::-1]

    def printStack(self):
        for i in self.items[::-1]:
            print(f"[{i}]")

    def push(self, item):
        if self.maxSize and len(self.items) > self.maxSize:
            self.popBottom()
        if item in self.items:
            self.items.remove(item)
            # self.push(",")
        return self.items.append(item)
