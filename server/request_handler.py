import socket
from _thread import *


class Server:
    def __init__(self):
        self.player_queue = []

    def player_thread(self, conn, ip, name):
        print("[SERVER][PLAYER] Starting new player thread.")

    def handle_queue(self):
        pass

    def authenticate(self, conn, addr):
        try:
            data = conn.recv(16)
            name = str(data.decode())
            if not name:
                raise Exception("No name recieved")

            conn.sendall("1")
            start_new_thread(self.player_thread, (conn, addr, name))
        except Exception as e:
            print("[EXEPTION]", e)
            conn.close()

    def connection_thread(self):
        server = ""
        port = 1234

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.bind((server, port))
        except socket.error as e:
            str(e)

        s.listen(2)
        print("[SERVER][CONNECTION] Waiting for connections, server started")

        while True:
            conn, addr = s.accept()
            print("[SERVER][CONNECTION] New connection to:", addr)

            self.authenticate(conn, addr)


if __name__ == "__main__":
    s = Server()
    start_new_thread(s.connection_thread, ())
