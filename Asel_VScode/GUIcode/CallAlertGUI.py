from PyQt5 import QtCore, QtGui, QtWidgets



class classCallAlertGUI(object):
    def __init__(self):
        super().__init__()

    def setupUi(self, callAlert,callPopupChoice,callerName):
        callAlert.setObjectName("callAlert")
        callAlert.resize(150, 140)
        callAlert.setStyleSheet("background-color: rgb(35,35,35);\n"
"")
        self.callerName = QtWidgets.QLabel(callAlert)
        self.callerName.setGeometry(QtCore.QRect(10, 10, 131, 71))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.callerName.setFont(font)
        self.callerName.setStyleSheet("color: white;\n"
"font-size:18;\n"
"highlight: white;")
        self.callerName.setObjectName("callerName")
        self.acceptCallButton = QtWidgets.QPushButton(callAlert)
        self.acceptCallButton.setGeometry(QtCore.QRect(90, 90, 41, 41))
        self.acceptCallButton.setToolTip("")
        self.acceptCallButton.setStyleSheet("QPushButton{\n"
"    background-color: rgb(48, 214, 76);\n"
"    border: 1px rgb(60,60,60);\n"
"    color: lime;\n"
"    font-size:12;\n"
"    highlight: white;\n"
"    border-radius:10px\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(80,80,80);\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: rgb(40,40,40);\n"
"}")
        self.acceptCallButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("GUIcode/icons/phone.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.acceptCallButton.setIcon(icon)
        self.acceptCallButton.setObjectName("acceptCallButton")
        self.declineCallButton = QtWidgets.QPushButton(callAlert)
        self.declineCallButton.setGeometry(QtCore.QRect(20, 90, 41, 41))
        self.declineCallButton.setToolTip("")
        self.declineCallButton.setStyleSheet("QPushButton{\n"
"    background-color: rgb(214, 47, 47);\n"
"    border: 1px rgb(60,60,60);\n"
"    color: lime;\n"
"    font-size:12;\n"
"    highlight: white;\n"
"    border-radius:10px\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(80,80,80);\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: rgb(40,40,40);\n"
"}")
        self.declineCallButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("GUIcode/icons/hangup.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.declineCallButton.setIcon(icon1)
        self.declineCallButton.setObjectName("declineCallButton")

        QtCore.QMetaObject.connectSlotsByName(callAlert)

        callAlert.setWindowTitle("callAlert")
        self.callerName.setText(f"<html><head/><body><p align=\"center\">{callerName}</p><p align=\"center\"><span style=\" font-size:9pt;\">incoming call...</span></p></body></html>")
        self.acceptCallButton.clicked.connect(lambda: callPopupChoice(True,callAlert))
        self.declineCallButton.clicked.connect(lambda: callPopupChoice(False,callAlert))
                

        

        #global globalCallAlertGUI
        #globalCallAlertGUI = self.callAlert
        