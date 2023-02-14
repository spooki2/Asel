import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 9002))

while True:
    message = input('Enter message: ')
    client_socket.sendall(message.encode())
    if message == 'exit':
        break
client_socket.close()
