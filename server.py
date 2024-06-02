import socket 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 1026))
server.listen()

client_socket, client_address = server.accept()

file = open("server_image.jpg", "wb")
imgChunk = client_socket.recv(2048)

while imgChunk:
    file.write(imgChunk)
    imgChunk = client_socket.recv(2048)


file.close()
client_socket.close()
