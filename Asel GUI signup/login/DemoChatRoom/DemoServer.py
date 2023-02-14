import threading
import socket

host = 'localhost'  # localhost
port = 20001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
usernames = []


def broadcast(msg, exclude=None):
    for B_client in clients:
        B_client.send(msg)
        #if B_client != exclude:
            #B_client.send(msg)


def handle(client):
    while True:
        try:
            msg = client.recv(1024)
            broadcast(msg,client)
        except:
            index = clients.index(client)
            clients.remove(client)  # removes the client from the index
            client.close()
            username = usernames[index]
            broadcast(f"<{username}> left the chat.".encode())  # leave msg
            usernames.remove(username)  # removes the username from the index
            break


def receive():
    while True:
        client, address = server.accept()
        print(f"connected with {str(address)}")

        client.send('NICK'.encode())  # keyword, not visible for the user [add to protocol]
        username = client.recv(1024).decode()
        usernames.append(username)
        clients.append(client)

        print(f"username: <{username}>")
        broadcast(f"<{username}> joined the chat!".encode())
        client.send('connected to the server!'.encode())

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is listening...")
receive()
