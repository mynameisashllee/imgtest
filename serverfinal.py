import socket
import os

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 5005))
server_socket.listen(5)

client_socket, address = server_socket.accept()
print("Connected to - ", address, "\n")

while True:
    choice = client_socket.recv(1024).decode()
    choice = int(choice)
    if choice == 1:
        data = client_socket.recv(1024).decode()
        print("The following data was received - ", data)
        print("Opening file - ", data)
        with open(data, 'r') as fp:
            strng = fp.read()
        size = os.path.getsize(data)
        size = str(size)
        client_socket.send(size.encode())
        client_socket.send(strng.encode())

    if choice == 2 or choice == 3:
        data = client_socket.recv(1024).decode()
        print("The following data was received - ", data)
        print("Opening file - ", data)
        with open(data, 'rb') as img:
            while True:
                strng = img.read(512)
                if not strng:
                    break
                client_socket.send(strng)
        print("Data sent successfully")
        exit()
