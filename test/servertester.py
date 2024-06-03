# ignore! not imp
import socket
import os

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_image_for_recipient(recipient, img_data):
    ensure_directory_exists(recipient)
    file_path = os.path.join(recipient, "server_image.jpg")

    with open(file_path, 'wb') as file:
        file.write(img_data)

def handle_client(client_socket):
    # receive username and recipient
    user_data = client_socket.recv(2048).decode().split('|')
    username = user_data[0]
    recipient = user_data[1]

    # receive image data
    img_data = bytearray()
    while True:
        chunk = client_socket.recv(2048)
        if not chunk:
            break
        img_data.extend(chunk)

    save_image_for_recipient(recipient, img_data)
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 1026))
    server.listen()

    while True:
        client_socket, client_address = server.accept()
        handle_client(client_socket)

if __name__ == '__main__':
    start_server()