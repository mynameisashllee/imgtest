# ignore! not imp
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 1026))

file = open('apple.jpeg', 'rb')
imgData = file.read(2048)

while imgData:
    client.send(imgData)
    imgData = file.read(2048)

file.close()
client.close()