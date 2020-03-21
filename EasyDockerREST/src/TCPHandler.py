import socket


class TCPConnection:
    def __init__(self, ip, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip, port))

    def send(self, message):
        self.s.send(message)

    def close(self):
        self.s.close()
