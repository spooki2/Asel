from PyQt5.QtWidgets import *
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap
import threading

app = QApplication([])
chat_app = QWidget()

# test mode#

import cv2
import numpy as np
## v this is the problem line
cap = cv2.VideoCapture(1)

cap = cv2.Video
#WTBfix -? #[cap= and all wtb()]
def WTB():
    #ret, frame = cap.read()
    #if not ret:
    #   return


    # convert the frame to bytes
    frame = cv2.resize(frame, (640, 480))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.array(frame)
    bytes_frame = frame.tobytes()
    return bytes_frame
    socket.send(f"CAM:{bytes_frame}".encode())


# cap.release()
# cv2.destroyAllWindows()


def ChatClient(username, ip, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))

    text = QTextEdit()
    text.setReadOnly(True)

    line = QLineEdit()
    label = QLabel()
    SendButtonClicked = False
    SendButton = QPushButton('Send')
    image = QLabel()
    pixmap = QPixmap("/home/ben/Desktop/meow.png")
    image.setPixmap(pixmap)

    right_layout = QVBoxLayout()
    right_layout.addWidget(text)
    right_layout.addWidget(line)
    right_layout.addWidget(SendButton)

    layout = QHBoxLayout()
    layout.addWidget(image)
    layout.addLayout(right_layout)
    cam = QPixmap('home/ben/Desktop/meow.png')
    label.setPixmap(cam)
    chat_app.setLayout(layout)
    chat_app.setWindowTitle("Chat")
    chat_app.setGeometry(100, 100, 400, 300)
    label.show()
    chat_app.show()

    def receive():
        while True:
            try:
                msg = client.recv(1024).decode()
                if msg == "NICK":
                    client.send(username.encode())
                    pass
                elif msg != "":
                    text.append(msg)
                elif msg[:4] == "CAM:":
                    msg = msg[:4]
                    print(f"CAM: {msg}")
            except:
                print("an error occurred")
                client.close()

    def write():
        client.send(f"CAM:{WTB()}".encode())

        msg = f'{username}: {line.text()}'
        client.send(msg.encode())

    SendButton.clicked.connect(write)

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()
