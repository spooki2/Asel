from PyQt5.QtWidgets import *
import socket
import os
import sys
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap
from ClientApplication import ChatClient
import ClientApplication

ip = "localhost"
port = 3000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, port))
# rem
app = QApplication([])




hashseed = os.getenv('PYTHONHASHSEED')
if not hashseed:
    os.environ['PYTHONHASHSEED'] = '0'
    os.execv(sys.executable, [sys.executable] + sys.argv)
# [9-12] settings to make hash consistent between runs

global LoginState
global RegState
LoginState = False
RegState = False

IntroScreen = QWidget()
IntroLayout = QGridLayout()
IntroLayout.addWidget(QLabel("Do You Have An Account?"))
GoRegButton = QPushButton("No, Register")
GoLoginButton = QPushButton("Yes, Login")
IntroLayout.addWidget(GoLoginButton)
IntroLayout.addWidget(GoRegButton)


def LoginClicked():
    IntroScreen.close()
    global LoginState
    LoginState = True
    LoginScreen.show()


def RegClicked():
    IntroScreen.close()
    global RegState
    RegState = True
    RegScreen.show()


IntroScreen.setLayout(IntroLayout)
GoLoginButton.clicked.connect(LoginClicked)
GoRegButton.clicked.connect(RegClicked)

L_Username = QLineEdit()
L_Password = QLineEdit()
R_Username = QLineEdit()
R_Password = QLineEdit()

RegScreen = QWidget()
RegScreen.resize(350, 110)
RegLayout = QGridLayout()
RegLayout.addWidget(QLabel("Username:"), 0, 0)
RegLayout.addWidget(R_Username, 0, 1)
RegLayout.addWidget(QLabel("Password:"), 1, 0)
RegLayout.addWidget(R_Password, 1, 1)
RegScreen.setLayout(RegLayout)

LoginScreen = QWidget()
LoginScreen.resize(350, 110)
LoginLayout = QGridLayout()
LoginLayout.addWidget(QLabel("Username:"), 0, 0)
LoginLayout.addWidget(L_Username, 0, 1)
LoginLayout.addWidget(QLabel("Password:"), 1, 0)
LoginLayout.addWidget(L_Password, 1, 1)
LoginScreen.setLayout(LoginLayout)

LoginButton = QPushButton("Login")

LoginButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
LoginLayout.addWidget(LoginButton, 2, 0, 1, 2)

GoRegButton.clicked.connect(RegClicked)
RegButton = QPushButton("Register")

RegButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
RegLayout.addWidget(RegButton, 2, 0, 1, 2)

IntroScreen.show()


class BreakIt(Exception):
    pass


alert = QMessageBox()
alert.setText('Invalid Username Or Password (Illegal Char)')
alert_reg = QMessageBox()
alert_reg.setText('Registered! You May Use These Details Next Time You Login')


def Login():
    L_username = L_Username.text()
    L_password = L_Password.text()
    try:
        print(L_username)
        if L_username.strip() == "":
            raise BreakIt
        for letter in L_username:
            if letter == ",":
                raise BreakIt
        for letter in L_password:
            if letter == ",":
                raise BreakIt
    except BreakIt:
        alert.exec()
        pass
    else:
        send = f"{hash(L_username)},{hash(L_password)}"
        client.send(send.encode())
        ValidLoginBool = client.recv(1024).decode()
        print(f"is login valid?: {ValidLoginBool}")
        if ValidLoginBool == "1":
            LoginScreen.close()
            print("ran chat client")
            ClientApplication.ChatClient(L_username, ip, port)


##the lien with chlientapp run


def Register():
    R_username = R_Username.text()
    R_password = R_Password.text()
    try:
        print(R_username)
        if R_username.strip() == "":
            raise BreakIt
        for letter in R_username:
            if letter == ",":
                raise BreakIt
        for letter in R_password:
            if letter == ",":
                raise BreakIt
        print("sent to serv")
    except BreakIt:
        alert.exec()
        pass
    else:
        send = f"R:{hash(R_username)},{hash(R_password)}"
        client.send(send.encode())
        alert_reg.exec()
        # client.close()
        global LoginState
        LoginState = False
        global RegState
        RegState = False
        print("rerunning")
        os.execv(sys.executable, ['python'] + sys.argv)


LoginButton.clicked.connect(Login)
RegButton.clicked.connect(Register)
app.exec()

#########################################################################
