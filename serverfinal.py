import socket
from PIL import Image
import imagehash
import os

def setup_problematic_img(hashfunc=imagehash.phash):
    directory = "problematic"  # directory of problematic images
    img_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.svg')
    problematic_img_hashes = []

    for file in os.listdir(directory):
        filename = os.path.join(directory, file).lower()
        if filename.endswith(img_formats):
            try:
                img_hash = hashfunc(Image.open(filename))
                problematic_img_hashes.append(img_hash)
            except Exception as e:
                print('Problem:', e, 'with', filename)
                continue
    
    return problematic_img_hashes

def check_img(problematic_img_hashes, img_hash_str, hashfunc=imagehash.phash, threshold=5):
    img_hash = imagehash.hex_to_hash(img_hash_str)
    for p_hash in problematic_img_hashes:
        if abs(img_hash - p_hash) <= threshold:
            return True
    return False

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 5005))
server_socket.listen(5)

problematic_img_hashes = setup_problematic_img()

while True:
    client_socket, address = server_socket.accept()
    print("Connected to - ", address, "\n")

    img_hash_str = client_socket.recv(1024).decode()

    if check_img(problematic_img_hashes, img_hash_str):
        client_socket.send("Image is problematic".encode())
        print("Img is problematic")
    else:
        client_socket.send("Image is OK".encode())
        print("Img is ok")
        
        # Receive the encrypted file
        encrypted_data = b''
        while True:
            strng = client_socket.recv(512)
            if not strng:
                break
            encrypted_data += strng

        client_socket.sendall(encrypted_data)
    
    print("data sent")
    client_socket.close()


