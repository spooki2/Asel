import socket
import random
import random
import traceback


# Generate a private key for use in the exchange.

aselModulus = 97
# large modulus number, used in all asel applications in all runs
aselBase = 2  # small number used as a base for computations,


# these do not cause a vulnerability


# simple symetric encryption
def encryptString(inputString, key):
    key = str(key)
    inputString = str(inputString)
    outputString = ""
    for i in range(len(inputString)):
        currentChar = inputString[i]
        currentKeyChar = key[i % len(key)]
        outputString += chr(ord(currentChar) ^ ord(currentKeyChar))
    return outputString


def decryptString(inputString, key):
    key = str(key)
    inputString = str(inputString)
    outputString = ""
    for i in range(len(inputString)):
        currentChar = inputString[i]
        currentKeyChar = key[i % len(key)]
        outputString += chr(ord(currentChar) ^ ord(currentKeyChar))
    return outputString


class hellmanClass:  # Diffie Hellman encryption/decryption built into a class, specifically for Asel
    def __init__(self, peerPublicKey):
        self.sharedKey = None
        self.privateKey = random.randint(100, 100000)
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
        return encryptString(data, self.sharedKey)

    def decrypt(self, data):
        return decryptString(data, self.sharedKey)

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
