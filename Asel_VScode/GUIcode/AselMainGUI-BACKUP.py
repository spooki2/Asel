from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from GUIcode import CSSdata

class AselMainGUI(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(AselMainGUI, self).__init__(*args, **kwargs)
        self.timer = QTimer() # initialize QTimer
        
    def setupUi(self, Asel,userLookup,sendMessage,refreshLite):
        global loadedText
        loadedText = None

        Asel.setObjectName("Asel")
        Asel.setEnabled(True)
        Asel.resize(560, 440)
        Asel.setStyleSheet("background-color: rgb(51,51,51);")
        self.centralwidget = QtWidgets.QWidget(Asel)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 561, 440))
        self.stackedWidget.setStyleSheet("")
        self.stackedWidget.setObjectName("stackedWidget")
        self.chatFrame = QtWidgets.QWidget()
        self.chatFrame.setObjectName("chatFrame")
        self.sendMsgButton = QtWidgets.QPushButton(self.chatFrame)
        self.sendMsgButton.setGeometry(QtCore.QRect(490, 390, 61, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.sendMsgButton.setFont(font)
        self.sendMsgButton.setStyleSheet(CSSdata.pushButtonCSS)
        self.sendMsgButton.setObjectName("sendMsgButton")
        self.msgLine = QtWidgets.QLineEdit(self.chatFrame)
        self.msgLine.setGeometry(QtCore.QRect(210, 390, 271, 41))
        self.msgLine.setStyleSheet(CSSdata.lineEditCSS)
        self.msgLine.setText("")
        self.msgLine.setObjectName("msgLine")
        self.textBox = QtWidgets.QTextEdit(self.chatFrame)
        self.textBox.setGeometry(QtCore.QRect(210, 10, 341, 371))
        self.textBox.setStyleSheet(CSSdata.lineEditCSS)
        self.textBox.setReadOnly(True)
        self.textBox.setObjectName("textBox")
        self.frame = QtWidgets.QFrame(self.chatFrame)
        self.frame.setGeometry(QtCore.QRect(10, 50, 191, 331))
        self.frame.setStyleSheet(CSSdata.frameCSS)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.friendBox1 = QtWidgets.QPushButton(self.frame)
        self.friendBox1.setGeometry(QtCore.QRect(10, 10, 171, 31))
        self.friendBox1.setStyleSheet(CSSdata.pushButtonCSS)
        self.friendBox1.setObjectName("friendBox1")
        self.friendBox6 = QtWidgets.QPushButton(self.frame)
        self.friendBox6.setGeometry(QtCore.QRect(10, 210, 171, 31))
        self.friendBox6.setStyleSheet(CSSdata.pushButtonCSS)
        self.friendBox6.setObjectName("friendBox6")
        self.friendBox5 = QtWidgets.QPushButton(self.frame)
        self.friendBox5.setGeometry(QtCore.QRect(10, 170, 171, 31))
        self.friendBox5.setStyleSheet(CSSdata.pushButtonCSS)
        self.friendBox2 = QtWidgets.QPushButton(self.frame)
        self.friendBox2.setGeometry(QtCore.QRect(10, 50, 171, 31))
        self.friendBox2.setObjectName("friendBox2")
        self.friendBox2.setStyleSheet(CSSdata.pushButtonCSS)
        self.friendBox4 = QtWidgets.QPushButton(self.frame)
        self.friendBox4.setGeometry(QtCore.QRect(10, 130, 171, 31))
        self.friendBox4.setStyleSheet(CSSdata.pushButtonCSS)
        self.friendBox4.setObjectName("friendBox4")
        self.friendBox3 = QtWidgets.QPushButton(self.frame)
        self.friendBox3.setGeometry(QtCore.QRect(10, 90, 171, 31))
        self.friendBox3.setStyleSheet(CSSdata.pushButtonCSS)
        self.friendBox3.setObjectName("friendBox3")
        self.friendBox7 = QtWidgets.QPushButton(self.frame)
        self.friendBox7.setGeometry(QtCore.QRect(10, 250, 171, 31))
        self.friendBox7.setStyleSheet(CSSdata.pushButtonCSS)
        self.friendBox7.setObjectName("friendBox7")
        self.friendBox8 = QtWidgets.QPushButton(self.frame)
        self.friendBox8.setGeometry(QtCore.QRect(10, 290, 171, 31))
        self.friendBox8.setStyleSheet(CSSdata.pushButtonCSS)
        self.friendBox8.setObjectName("friendBox8")
        self.userLine = QtWidgets.QLineEdit(self.chatFrame)
        self.userLine.setGeometry(QtCore.QRect(10, 10, 191, 31))
        self.userLine.setStyleSheet(CSSdata.lineEditCSS)
        self.userLine.setText("")
        self.userLine.setObjectName("userLine")
        self.callButton = QtWidgets.QPushButton(self.chatFrame)
        self.callButton.setGeometry(QtCore.QRect(520, 20, 21, 21))
        self.callButton.setToolTip("")
        self.callButton.setStyleSheet(CSSdata.callButtonCSS)
        self.callButton.setText("")
        icon = QtGui.QIcon.fromTheme("call")
        self.callButton.setIcon(icon)
        self.callButton.setObjectName("callButton")
        self.stackedWidget.addWidget(self.chatFrame)
        self.mainPage = QtWidgets.QWidget()
        self.mainPage.setObjectName("mainPage")
        
        self.stackedWidget.addWidget(self.mainPage)
        Asel.setCentralWidget(self.centralwidget)

        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Asel)

        Asel.setWindowTitle("Asel")
        self.sendMsgButton.setText("send")
        self.msgLine.setPlaceholderText(" Send a message...")
        self.textBox.setStyleSheet(CSSdata.lineEditCSS)
        self.userLine.setPlaceholderText(" Search a user...")
        global globalTextBox
        globalTextBox = self.textBox
        global globalFriendBoxes
        globalFriendBoxes = [self.friendBox1,self.friendBox2,self.friendBox3,self.friendBox4,self.friendBox5,self.friendBox6,self.friendBox7,self.friendBox8]
        def userLookupCall(str):
            userLookup(str)
        
        self.friendBox1.clicked.connect(lambda: userLookupCall(self.friendBox1.text()))
        self.friendBox2.clicked.connect(lambda: userLookupCall(self.friendBox2.text()))
        self.friendBox3.clicked.connect(lambda: userLookupCall(self.friendBox3.text()))
        self.friendBox4.clicked.connect(lambda: userLookupCall(self.friendBox4.text()))
        self.friendBox5.clicked.connect(lambda: userLookupCall(self.friendBox5.text()))
        self.friendBox6.clicked.connect(lambda: userLookupCall(self.friendBox6.text()))
        self.friendBox7.clicked.connect(lambda: userLookupCall(self.friendBox7.text()))
        self.friendBox8.clicked.connect(lambda: userLookupCall(self.friendBox8.text()))
        
        def userLookupStorage():
            #global userLookupName
            userLookupName = self.userLine.text()
            userLookup(self.userLine.text())
        def messageStorage():
            sendMessage(self.msgLine.text())
        self.userLine.returnPressed.connect(userLookupStorage)
        self.sendMsgButton.clicked.connect(messageStorage)

        self.timer.timeout.connect(refreshLite)
        self.timer.start(10)




