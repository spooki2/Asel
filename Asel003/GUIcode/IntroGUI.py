from PyQt5 import QtCore, QtGui, QtWidgets
from GUIcode import CSSdata


class IntroGUI:
    def setupUi(self,intro,regChoice,logChoice):
        intro.setObjectName("intro")
        intro.resize(190, 130)
        intro.setStyleSheet("background-color: rgb(51,51,51);")
        self.centralwidget = QtWidgets.QWidget(intro)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 50, 111, 31))
        self.pushButton.setStyleSheet(CSSdata.pushButtonCSS)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(40, 90, 111, 31))
        self.pushButton_2.setStyleSheet(CSSdata.pushButtonCSS)
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setMouseTracking(False)
        self.label.setStyleSheet("color: white;")
        self.label.setObjectName("label")
        intro.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(intro)
        intro.setWindowTitle( "Asel")
        self.pushButton.setText("Register")
        self.pushButton_2.setText("Login")
        self.label.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">Welcome To Asel!</span></p></body></html>")
        #self.pushButton.clicked.connect(regChoice)
        self.pushButton.clicked.connect(regChoice)
        self.pushButton_2.clicked.connect(logChoice) #callback functions to which button was clicked
        global introGlobal
        introGlobal = intro
