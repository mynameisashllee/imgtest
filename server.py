import socket 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 1025))

server.listen()

BUFFER_SIZE = 4096

while True:
    client_socket, client_address = server.accept()

    with open("server_image.jpg", "wb") as file:
        recvData = client_socket.recv(BUFFER_SIZE)
        while recvData:
            file.write(recvData)
            recvData = client_socket.recv(BUFFER_SIZE)
