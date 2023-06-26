"""
File to handle communication with the server
"""
import socket
import json


class Client:
    addr = "localhost"
    port = 1701

    def __init__(self, game):
        self.game = game
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        self.client.connect((self.addr, self.port))
        self.send(self.game.name)
        r = self.client.recv(16).decode()
        if r == "0":
            print(f"[CONNECTION] Connected to server at ip: {self.addr}, port: {self.port}")
        else:
            print(f"[EXCEPTION] Failed to connect: invalid name")

    def send(self, packet):
        try:
            self.client.sendall(json.dumps(packet).encode())
            print("[LOG] Sent packet to server")

            reply = json.load(self.client.recv(1024).decode())
            print(reply)
            return reply
        except Exception as e:
            print("[EXCEPTION] Error sending a packet")
            self.disconnect(e)

    def disconnect(self, msg):
        self.client.close()
        print("[EXCEPTION] Client disconnected from server:", msg)


if __name__ == "__main__":
    class G:
        name = "Miles"
    g = G()
    c = Client(g)

    # c.send({
