import threading
import socket

host = "127.0.0.1"
port = 49999

# TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message.encode("ascii"))


# for each client, run handle(client) function
def handle(client):
    while True:
        try:
            # Receive message from a client and then broadcast the message
            # to all clients
            message = client.recv(1024).decode("ascii")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat!")
            nicknames.remove(nickname)
            break


def receive():
    while True:
        # Wait for an incoming connection.
        # Return a new socket representing the connection,
        # and the address of the client.
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("NICK".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat")
        print("Current users in the chat room: ", nicknames)
        client.send("Connected to the server!".encode("ascii"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print(f"Server is listening on port {port}")
receive()
