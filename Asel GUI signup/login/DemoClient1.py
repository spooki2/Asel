import sys
from PyQt5.QtWidgets import QApplication, QTextEdit, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QPixmap
import WebcamToByte
import threading

app = QApplication(sys.argv)

text = QTextEdit()
text.setReadOnly(True)

line = QLineEdit()

button = QPushButton('Send')
button.clicked.connect(lambda: text.append(line.text()) or line.clear())

image = QLabel()
pixmap = QPixmap("/home/ben/Desktop/meow.png")
image.setPixmap(pixmap)


right_layout = QVBoxLayout()
right_layout.addWidget(text)
right_layout.addWidget(line)
right_layout.addWidget(button)

layout = QHBoxLayout()
layout.addWidget(image)
layout.addLayout(right_layout)

chat_app = QWidget()
chat_app.setLayout(layout)
chat_app.setWindowTitle("Chat")
chat_app.setGeometry(100, 100, 400, 300)
chat_app.show()



sys.exit(app.exec_())
