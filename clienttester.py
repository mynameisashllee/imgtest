import socket

def register_and_send_image(username, recipient, file_path):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 1026))

    # send username and recipient
    client.send(f'{username}|{recipient}'.encode())

    # send image file
    with open(file_path, 'rb') as file:
        img_data = file.read(2048)
        while img_data:
            client.send(img_data)
            img_data = file.read(2048)

    client.close()

if __name__ == '__main__':
    username = input("Enter your username: ")
    recipient = input("Enter the recipient's username: ")
    file_path = input("Enter the image file path: ")

    register_and_send_image(username, recipient, file_path)