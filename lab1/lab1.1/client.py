import socket

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((SERVER_IP, SERVER_PORT))

while True:
    message = input("Уведіть речення для відправки на сервер (або 'вихід', щоб вийти): ")

    if message.lower() == 'вихід':
        print("Прощавай!")
        break

    client_socket.send(message.encode('utf-8'))

client_socket.close()