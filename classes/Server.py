from .Message import Message
import socket
import threading
import struct
import os
from Crypto.Cipher import AES
from PIL import Image
import imagehash

class Server:
    def __init__(self):
        self.clients = {}
        self.problematic_img_hashes = self.setup_problematic_img()

    def setup_problematic_img(self, hashfunc=imagehash.phash):
        directory = os.fsencode("problematic")  # Change this to the directory of problematic images
        img_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.svg')
        problematic_img_hashes = []

        for file in os.listdir(directory):
            dir_str = os.fsdecode(directory).lower()
            filename = os.fsdecode(file).lower()
            if filename.endswith(img_formats):
                try:
                    hash = hashfunc(Image.open(os.path.join(dir_str, filename)))
                    problematic_img_hashes.append(hash)
                except Exception as e:
                    print('Problem:', e, 'with', filename)
                    continue

        return problematic_img_hashes

    def check_img(self, img_data, hashfunc=imagehash.phash):
        try:
            img = Image.open(img_data)
            hash = hashfunc(img)
        except Exception as e:
            print('Error occurred with reading file:', e)
            return False
        
        if hash in self.problematic_img_hashes:
            print("Image is problematic")
            return True
        else:
            print("Image is OK")
            return False

    def handle_client(self, client_socket, client_address):
        print(f"Connected to {client_address}")
        client_id = None
        try:
            while True:
                raw_msglen = self.recvall(client_socket, 4)
                if not raw_msglen:
                    break
                msglen = struct.unpack('>I', raw_msglen)[0]
                data = self.recvall(client_socket, msglen)
                if not data:
                    break

                if client_id is None:
                    client_id = data.decode('utf-8')
                    self.clients[client_id] = client_socket
                    print(f"Registered client {client_id} at {client_address}")
                    continue

                message = Message()
                message.bytes_to_msg(data)
                packet = message.get_packet_data()

                dest_id = packet['dest_id']
                if self.check_img(packet['payload']):
                    print(f"Received a problematic image from {client_id}.")
                    # Handle the problematic image as needed (e.g., log, discard, etc.)
                else:
                    if dest_id in self.clients:
                        self.save_image(packet['payload'], packet['nonce'], client_id)
                        self.send_to_client(dest_id, raw_msglen + data)
                    else:
                        print(f"No client with ID {dest_id} found.")
        except socket.error:
            pass
        finally:
            if client_id and client_id in self.clients:
                del self.clients[client_id]
                print(f"Client {client_id} disconnected.")
            client_socket.close()

    def send_to_client(self, client_id, message):
        client_socket = self.clients.get(client_id)
        if client_socket:
            try:
                client_socket.send(message)
            except socket.error as e:
                print(f"Error sending message to {client_id}: {e}")

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', 9999))
        server_socket.listen(5)
        print("Server is listening on port 9999...")

        try:
            while True:
                client_socket, addr = server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket, addr)).start()
        finally:
            server_socket.close()

    def save_image(self, ct, nonce, client_id):
        image_data = self.dec(ct, nonce)
        folder_path = os.path.join("received_images", client_id)
        os.makedirs(folder_path, exist_ok=True)
        image_path = os.path.join(folder_path, f"received_from_{client_id}.jpg")
        with open(image_path, "wb") as image_file:
            image_file.write(image_data)
        print(f"Image received from {client_id} saved as {image_path}")

    def recvall(self, sock, n):
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

    def dec(self, ct, nonce):
        cipher = AES.new(self.enc_key, AES.MODE_EAX, nonce=nonce)
        message = cipher.decrypt(ct)
        return message
