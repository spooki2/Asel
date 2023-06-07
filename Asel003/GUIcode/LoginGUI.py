from PyQt5 import QtCore, QtGui, QtWidgets
from GUIcode import CSSdata


class LoginGUI():
    def setupUi(self, login, loginSubmit):
        login.setObjectName("login")
        login.resize(240, 120)
        login.setMouseTracking(False)
        login.setWindowOpacity(1.0)
        login.setAutoFillBackground(False)
        login.setStyleSheet("background-color: rgb(51,51,51);")
        login.setAnimated(True)
        login.setDocumentMode(False)
        login.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(login)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 10, 81, 21))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(90, 10, 141, 20))
        self.lineEdit.setStyleSheet(CSSdata.lineEditCSS)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(90, 40, 141, 20))
        self.lineEdit_2.setStyleSheet(CSSdata.lineEditCSS)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 40, 81, 20))
        self.label_2.setObjectName("label_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 70, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet(CSSdata.pushButtonCSS)
        self.pushButton_2.setObjectName("pushButton_2")
        login.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(login)

        login.setWindowTitle("Asel")
        self.label.setText(
            "<html><head/><body><p align=\"right\"><span style=\" font-size:12pt; color:#ffffff;\">Username:</span></p></body></html>")
        self.label_2.setText(
            "<html><head/><body><p align=\"right\"><span style=\" font-size:12pt; color:#ffffff;\">Password:</span></p></body></html>")
        self.pushButton_2.setText("Login")

        def infoStorage():
            global username
            global password
            username = self.lineEdit.text()
            password = self.lineEdit_2.text()
            loginSubmit()

        self.pushButton_2.clicked.connect(infoStorage)  # sets name and pass and then callback button press
        global loginGlobal
        loginGlobal = login  # object in global form
