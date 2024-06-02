from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import threading
import socket
from .Message import Message
import os
import struct

class Client:
    def __init__(self, enc_key):
        self.enc_key = enc_key
        if len(self.enc_key) < 16:
            for i in range(16 - len(self.enc_key)):
                self.enc_key += "0"
        elif len(self.enc_key) > 16:
            self.enc_key = self.enc_key[0:16]
        self.enc_key = self.enc_key.encode('utf-8')

    def receive_message(self, client_socket):
        while True:
            try:
                raw_msglen = self.recvall(client_socket, 4)
                if not raw_msglen:
                    print("Server disconnected.")
                    break
                msglen = struct.unpack('>I', raw_msglen)[0]
                data = self.recvall(client_socket, msglen)
                message = Message()
                message.bytes_to_msg(data)
                packet = message.get_packet_data()

                dest_id = packet['dest_id']
                image_data = self.dec(packet['payload'], packet['nonce'])
                with open(f"received_{dest_id}.jpg", "wb") as image_file:
                    image_file.write(image_data)
                print(f"\nReceived an image from {dest_id} and saved as received_{dest_id}.jpg")

            except socket.error:
                print("Error receiving data")
                break

    def send_messages(self, client_socket):
        while True:
            try:
                recipient_id = input("Enter recipient ID: ")
                image_path = input("Enter image path: ")
                if not os.path.isfile(image_path):
                    print("Invalid file path. Please try again.")
                    continue
                with open(image_path, "rb") as image_file:
                    image_data = image_file.read()
                packet = Message()
                nonce = get_random_bytes(16)
                ct = self.enc(image_data, nonce)
                packet.update_data(recipient_id, ct, nonce)
                byte_arr = packet.msg_to_bytes()
                msglen = struct.pack('>I', len(byte_arr))
                client_socket.sendall(msglen + byte_arr)
                print(f"Sent image to {recipient_id}")

            except KeyboardInterrupt:
                print("Exiting...")
                break

            except socket.error:
                print("Error sending message.")
                break

    def start_client(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect(('127.0.0.1', 9999))
        except socket.error as e:
            print(f"Cannot connect to the server: {e}")
            return

        self.client_id = input("Enter your client ID: ")
        client_socket.sendall(self.client_id.encode())

        threading.Thread(target=self.receive_message, args=(client_socket,), daemon=True).start()
        while True:
            try:
                self.send_messages(client_socket)
            finally:
                client_socket.close()
                print("Connection closed.")

    def enc(self, message, nonce):
        assert len(self.enc_key) == 16
        cipher = AES.new(self.enc_key, AES.MODE_EAX, nonce=nonce)
        ct = cipher.encrypt(message)
        return ct

    def dec(self, ct, nonce):
        assert len(self.enc_key) == 16
        cipher = AES.new(self.enc_key, AES.MODE_EAX, nonce=nonce)
        message = cipher.decrypt(ct)
        return message

    def recvall(self, sock, n):
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data