from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from GUIcode import CSSdata
from GUIcode import CallAlertGUI
from PyQt5.QtCore import QThread, pyqtSignal


class AselMainGUIclass(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(AselMainGUIclass, self).__init__(*args, **kwargs)
        self.timer = QTimer()  # initialize QTimer

    def callAlertInit(self, callPopupChoice, callerName):
        self.window = QtWidgets.QMainWindow()
        self.ui = CallAlertGUI.classCallAlertGUI()
        self.ui.setupUi(self.window, callPopupChoice, callerName)
        self.window.show()

    def setupUi(self, Asel, userLookup, sendMessage, refreshLite, callRequest, checkIfCalled, callerName, initCallFunc,
                updateCamFeed, killCall, checkIfCallEnded, checkIfMuted, aboutToClose):
        global loadedText
        loadedText = None
        global camToggle
        camToggle = True
        global muteToggle
        muteToggle = False
        Asel.setObjectName("Asel")
        Asel.setEnabled(True)
        Asel.resize(560, 440)
        Asel.setStyleSheet("background-color: rgb(51,51,51);")
        self.centralwidget = QtWidgets.QWidget(Asel)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 561, 440))
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
        self.userLine.setObjectName("userLine")
        self.callButton = QtWidgets.QPushButton(self.chatFrame)
        self.callButton.setGeometry(QtCore.QRect(520, 20, 21, 21))
        self.callButton.setStyleSheet(CSSdata.callButtonCSS)
        icon = QtGui.QIcon.fromTheme("call")
        self.callButton.setIcon(icon)
        self.callButton.setObjectName("callButton")
        self.stackedWidget.addWidget(self.chatFrame)
        self.vcPage = QtWidgets.QWidget()
        self.vcPage.setObjectName("mainPage")
        self.camFrame = QtWidgets.QFrame(self.vcPage)
        self.camFrame.setGeometry(QtCore.QRect(10, 10, 541, 361))
        self.camFrame.setStyleSheet(CSSdata.frameCSS)
        self.camFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.camFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.camFrame.setObjectName("camFrame")
        self.webCam = QtWidgets.QLabel(self.camFrame)
        self.webCam.setGeometry(QtCore.QRect(100, 10, 341, 341))
        self.webCam.setPixmap(QtGui.QPixmap("GUIcode/icons/cameraOff.png"))
        self.webCam.setObjectName("Webcam")
        self.hangUpCallButton = QtWidgets.QPushButton(self.vcPage)
        self.hangUpCallButton.setGeometry(QtCore.QRect(450, 380, 101, 51))
        self.hangUpCallButton.setStyleSheet(CSSdata.hangUpCallCSS)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("GUIcode/icons/hangup.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.hangUpCallButton.setIcon(icon1)
        self.hangUpCallButton.setObjectName("hangUpCallButton")
        self.muteButton = QtWidgets.QPushButton(self.vcPage)
        self.muteButton.setGeometry(QtCore.QRect(330, 380, 51, 51))
        self.muteButton.setStyleSheet(CSSdata.utilityButtonCSS)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("GUIcode/icons/mic.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.muteButton.setIcon(icon2)
        self.muteButton.setObjectName("muteButton")
        self.cameraButton = QtWidgets.QPushButton(self.vcPage)
        self.cameraButton.setGeometry(QtCore.QRect(390, 380, 51, 51))
        self.cameraButton.setStyleSheet(CSSdata.utilityButtonCSS)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("GUIcode/icons/camera.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cameraButton.setIcon(icon3)
        self.cameraButton.setObjectName("cameraButton")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("GUIcode/icons/avatar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stackedWidget.addWidget(self.chatFrame)
        Asel.setCentralWidget(self.centralwidget)

        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Asel)

        self.stackedWidget.addWidget(self.vcPage)
        Asel.setCentralWidget(self.centralwidget)

        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Asel)

        Asel.setWindowTitle("Asel")
        self.sendMsgButton.setText("send")
        self.msgLine.setPlaceholderText(" Send a message...")
        self.textBox.setStyleSheet(CSSdata.lineEditCSS)
        self.userLine.setPlaceholderText(" Search a user...")

        global globalWebCam

        globalWebCam = self.webCam
        global globalStackedWidget
        globalStackedWidget = self.stackedWidget
        global globalTextBox
        globalTextBox = self.textBox
        global globalFriendBoxes
        globalFriendBoxes = [self.friendBox1, self.friendBox2, self.friendBox3, self.friendBox4, self.friendBox5,
                             self.friendBox6, self.friendBox7, self.friendBox8]

        def userLookupCall(str):
            userLookup(str)

        #self.aboutToQuit.connect(aboutToClose)
        self.friendBox1.clicked.connect(lambda: userLookupCall(self.friendBox1.text()))
        self.friendBox2.clicked.connect(lambda: userLookupCall(self.friendBox2.text()))
        self.friendBox3.clicked.connect(lambda: userLookupCall(self.friendBox3.text()))
        self.friendBox4.clicked.connect(lambda: userLookupCall(self.friendBox4.text()))
        self.friendBox5.clicked.connect(lambda: userLookupCall(self.friendBox5.text()))
        self.friendBox6.clicked.connect(lambda: userLookupCall(self.friendBox6.text()))
        self.friendBox7.clicked.connect(lambda: userLookupCall(self.friendBox7.text()))
        self.friendBox8.clicked.connect(lambda: userLookupCall(self.friendBox8.text()))

        self.callButton.clicked.connect(callRequest)

        # self.callButton.clicked.connect(lambda: self.callAlertInit())
        # self.callButton.clicked.connect(test)

        def userLookupStorage():
            # global userLookupName
            userLookupName = self.userLine.text()
            userLookup(self.userLine.text())

        def messageStorage():
            sendMessage(self.msgLine.text())

        self.userLine.returnPressed.connect(userLookupStorage)
        self.sendMsgButton.clicked.connect(messageStorage)

        def camToggleLogic():
            global camToggle
            if camToggle:
                camToggle = False
            else:
                camToggle = True

        def micToggleLogic():
            global muteToggle
            if muteToggle:
                muteToggle = False
            else:
                muteToggle = True

        global globalMuteButton
        globalMuteButton = self.muteButton
        global globalCamButton
        globalCamButton = self.cameraButton

        self.cameraButton.clicked.connect(camToggleLogic)
        self.muteButton.clicked.connect(micToggleLogic)
        self.hangUpCallButton.clicked.connect(killCall)
        self.timer.timeout.connect(checkIfCalled)
        self.timer.timeout.connect(checkIfCallEnded)
        self.timer.timeout.connect(refreshLite)
        self.timer.timeout.connect(initCallFunc)
        self.timer.timeout.connect(lambda: updateCamFeed(camToggle))
        self.timer.timeout.connect(lambda: checkIfMuted(muteToggle))
        self.timer.start(10)
