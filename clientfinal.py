#!/usr/bin/python3
# TCP client example
import socket
import os

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 5005))
k = ' '
size = 1024

while True:
    print("Do you want to transfer a \n1.Text File\n2.Image\n3.Video\n")
    k = input()
    client_socket.send(k.encode())
    k = int(k)
    if k == 1:
        print("Enter file name\n")
        strng = input()
        client_socket.send(strng.encode())
        size = client_socket.recv(1024).decode()
        size = int(size)
        print("The file size is - ", size, " bytes")
        strng = client_socket.recv(size).decode()
        print("\nThe contents of that file - ")
        print(strng)

    if k == 2 or k == 3:
        print("Enter file name of the image with extension (example: filename.jpg, filename.png or if a video file then filename.mpg etc) - ")
        fname = input()
        client_socket.send(fname.encode())
        with open(fname, 'wb') as fp:
            while True:
                strng = client_socket.recv(512)
                if not strng:
                    break
                fp.write(strng)
        print("Data Received successfully")
        
        # open the image
        if os.name == 'nt':  # windows
            os.system(f'start {fname}')
        elif os.name == 'posix':  # linux/mac
            os.system(f'open {fname}')
        exit()
