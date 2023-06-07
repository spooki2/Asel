from PyQt5 import QtCore, QtGui, QtWidgets
from GUIcode import CSSdata


class AlertGUI():
    def setupUi(self, alert, okButton, bigLabel, smallLabel, buttonText):
        alert.setObjectName("Asel")
        alert.resize(200, 120)
        alert.setStyleSheet("background-color: rgb(51,51,51);")
        self.centralwidget = QtWidgets.QWidget(alert)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setMouseTracking(True)
        self.label.setStyleSheet("color: white;")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 181, 40))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setMouseTracking(True)
        self.label_2.setStyleSheet("color: white;")
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(50, 80, 101, 31))
        self.pushButton.setStyleSheet(CSSdata.pushButtonCSS)
        self.pushButton.setObjectName("pushButton")
        alert.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(alert)
        alert.setWindowTitle("Asel")
        self.label.setText(
            f"<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">{bigLabel}</span></p></body></html>")
        self.label_2.setText(
            f"<html><head/><body><p align=\"center\"><span style=\" font-size:8pt;\">{smallLabel}</span></p></body></html>")
        self.pushButton.setText(buttonText)
        self.pushButton.clicked.connect(okButton)
        global alertGlobal
        alertGlobal = alert  # object in global form
