import socket
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from PIL import Image
import imagehash

# Encryption key (must be 16, 24, or 32 bytes long)
key = b'Sixteen byte key'
iv = get_random_bytes(16)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 5005))

def encrypt_image(fname):
    with open(fname, 'rb') as fp:
        original_data = fp.read()
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted_data = cipher.encrypt(pad(original_data, AES.block_size))
    return encrypted_data

def hash_image(fname, hashfunc=imagehash.phash):
    img = Image.open(fname)
    return hashfunc(img)

def decrypt_image(encrypted_data):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data

while True:
    print("Enter file name")
    fname = input()

    # Hash the original image
    img_hash = hash_image(fname)
    client_socket.send(str(img_hash).encode())

    # Receive server response
    response = client_socket.recv(1024).decode()
    if response == "Image is problematic":
        print("Image is problematic")
    else:
        # Encrypt the image
        encrypted_data = encrypt_image(fname)
        
        # Send the encrypted image file
        client_socket.sendall(encrypted_data)
        print("Data sent successfully")

        received_encrypted_data = b''
        while True:
            strng = client_socket.recv(512)
            if not strng:
                break
            received_encrypted_data += strng

        print("data got agn")

        # Decrypt the received encrypted data
        decrypted_data = decrypt_image(received_encrypted_data)
        print("decrypted")
        
        # Save the decrypted file
        decrypted_fname = "decrypted_" + fname
        with open(decrypted_fname, 'wb') as dfp:
            dfp.write(decrypted_data)

        print("Data received and decrypted successfully")
    
    exit()
