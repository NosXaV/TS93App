
import socket
import json

class PhoenixBotClient:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        self.socket = socket.create_connection((self.host, self.port))

    def send_message(self, message):
        if self.socket:
            msg = json.dumps(message) + '\x01'
            self.socket.sendall(msg.encode('utf-8'))

    def close(self):
        if self.socket:
            self.socket.close()
