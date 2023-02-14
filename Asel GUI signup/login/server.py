import socket
import threading

try:
    host = 'localhost'  # localhost
    port = 3000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()


    def LoginServer(ServerStopRun=False):
        while not ServerStopRun:
            (client_socket, client_address) = server.accept()
            HashRequest = ""
            ValidLogin = False

            client_socket, client_address = server.accept()
            request = client_socket.recv(1024)
            HashRequest = request.decode()
            HashRequest = str(HashRequest).strip()

            if HashRequest[:2] == "R:":
                print(f"package[R]: {HashRequest}")
                HashRequest = HashRequest[2:]
                with open('UserDataBase.txt', "a+") as f:
                    f.write(f"\n{HashRequest}")

            else:
                print(f"package[L]: {HashRequest}")
                with open('UserDataBase.txt') as f:
                    lines = f.readlines()
                    for line in lines:
                        if line == HashRequest:
                            ValidLogin = True
                    print(f"Found Login?: {ValidLogin}")
                    if ValidLogin:
                        ServerStopRun = True
                        client_socket.send("1".encode())
                        ChatServerThread.start()
                    if not ValidLogin:
                        client_socket.send("0".encode())


    #########################################################################

    def ChatServer():
        clients = []
        usernames = []

        def broadcast(msg, exclude=None):
            for B_client in clients:
                B_client.send(msg)
                # if B_client != exclude:
                # B_client.send(msg)

        def handle(client):
            while True:
                try:
                    msg = client.recv(1024)
                    broadcast(msg, client)
                except:
                    # send Camera Info
                    if msg[:4] == "CAM:":
                        msg = msg[:4]
                        print(f"package[CAM]: {msg}")
                        broadcast(f"CAM:{msg}")

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
                broadcast(f"<{username}> joined the chat!\n".encode())
                client.send('connected to the server!'.encode())

                thread = threading.Thread(target=handle, args=(client,))
                thread.start()

        print("Server is listening...")
        receive()


    # Initiating The Threads

    LoginServerThread = threading.Thread(target=LoginServer)
    ChatServerThread = threading.Thread(target=ChatServer)

    LoginServerThread.start()
except:
    socket.close()
