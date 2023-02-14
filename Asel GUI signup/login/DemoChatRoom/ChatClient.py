from PyQt5.QtWidgets import QApplication, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget
import socket
import threading


def ChatClient(username, ip, port):
    app = QApplication([])
    text = QTextEdit()
    text.setReadOnly(True)

    line = QLineEdit()
    SendButtonClicked = False
    SendButton = QPushButton('Send')
    layout = QVBoxLayout()
    layout.addWidget(text)
    layout.addWidget(line)
    layout.addWidget(SendButton)

    chat_app = QWidget()
    chat_app.setLayout(layout)
    chat_app.setWindowTitle("Chat")
    chat_app.setGeometry(100, 100, 400, 300)
    chat_app.show()

    ####################################

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))

    def receive():
        while True:
            try:
                msg = client.recv(1024).decode()
                if msg == "NICK":
                    client.send(username.encode())
                    pass
                elif msg != "":
                    text.append(msg)
            except:
                print("an error occurred")
                client.close()

    def write():
        msg = f'{username}: {line.text()}'
        client.send(msg.encode())

    SendButton.clicked.connect(write)

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()
    ###
    app.exec()

