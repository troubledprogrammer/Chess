"""
File to handle communication with the server
"""
import socket


class Client:
    addr = "192.168.0.36"
    port = 5555

    def __init__(self, game):
        self.game = game
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.addr, self.port))
        print(f"[CLIENT] Connected to server at ip: {self.addr}, port: {self.port}")

    def send(self, packet):
        self.client.sendall(packet.encode())
        print("[CLIENT] Sent packet to server")
