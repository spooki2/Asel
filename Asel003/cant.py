string = "hi"
key = 421


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


e = encryptString(string, key)
print(e)
print(decryptString(e, key))
