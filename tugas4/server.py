import logging
import socket
import sys
import threading
from datetime import datetime
from struct import pack, unpack
from typing import Optional

from deps.config import Config
from deps.utils import Action, Packet

config = Config()

class ClientHandler(threading.Thread):
    def __init__(self, conn: socket.socket, address: str):
        self.conn: socket.socket = conn
        self.address: str = address
        super().__init__()

    def send(self, packet: Packet) -> None:
        logging.info(f"Sending response packet {packet}")
        self.conn.sendall(packet.json.encode())
        self.conn.shutdown(socket.SHUT_WR)

    def recv(self) -> Optional[Packet]:
        data = b''
        while True:
            data_rcv = self.conn.recv(Packet.BUFFER)
            data += data_rcv
            if not data_rcv:
                break
        try:
            packet = Packet().from_json(data.decode())
            return packet
        except Exception as e:
            logging.error(f'recv: {e}')
            return None

    def run(self):
        while True:
            req = self.recv()
            logging.info(req.cmd)
            if req and req.cmd:
                if Action[req.cmd] == Action.LIST:
                    packet = Packet(req.cmd, config.config["dir"])
                    print("AS")
                    self.send(packet.result)
                    break
                break
            else:
                break


        self.conn.close()

class Server(threading.Thread):
    def __init__(self):
        self.clients = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        super().__init__()

    def run(self):
        self.sock.bind((config.config["host"], config.config["port"]))
        self.sock.listen()

        while(True):
            conn, addr = self.sock.accept()
            logging.info(f"Connection from {addr}")

            client = ClientHandler(conn, addr)
            client.start()
            self.clients.append(client)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    Server().start()