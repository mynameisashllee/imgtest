import marshal

class Message:
    def __init__(self):
        pass

    def update_dest_id(self, dest_id):
        self.dest_id = dest_id

    def update_payload(self, payload):
        self.payload = payload

    def update_nonce(self, nonce):
        self.nonce = nonce

    def update_data(self, dest_id, payload, nonce):
        self.update_dest_id(dest_id)
        self.update_payload(payload)
        self.update_nonce(nonce)

    def get_packet_data(self):
        packet_data = {
            'dest_id': self.dest_id,
            'payload': self.payload,
            'nonce': self.nonce,
        }
        return packet_data

    def msg_to_bytes(self):
        return marshal.dumps(self.get_packet_data())

    def bytes_to_msg(self, input_bytes):
        unmarshalled_data = marshal.loads(input_bytes)
        self.dest_id = unmarshalled_data['dest_id']
        self.payload = unmarshalled_data['payload']
        self.nonce = unmarshalled_data['nonce']
