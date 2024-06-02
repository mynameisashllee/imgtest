from .Message import Message
import socket
import threading
import struct

class Server:
    def __init__(self):
        self.clients = {}

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
                if dest_id in self.clients:
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
                client_socket.sendall(message)
                print(f"Sent image to client {client_id}")
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

    def recvall(self, sock, n):
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data
