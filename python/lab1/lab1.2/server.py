import socket
import threading

HOST = socket.gethostname()
PORT = 5050
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} вийшов!'.encode(FORMAT))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, addr = server.accept()
        print(f"Підключився за адресою: {addr}")

        client.send('NICK'.encode(FORMAT))
        nickname = client.recv(1024).decode(FORMAT)
        nicknames.append(nickname)
        clients.append(client)

        print(f"Ваше нікнейм {nickname}")
        broadcast(f"{nickname} приєднався!".encode(FORMAT))
        client.send('Приєднався до серверу!'.encode(FORMAT))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()