import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 1025))

BUFFER_SIZE = 4096

with open('apple.jpeg', 'rb') as file:
    imgData = file.read(BUFFER_SIZE)

    while imgData:
        client.send(imgData)
        imgData = file.read(BUFFER_SIZE)
