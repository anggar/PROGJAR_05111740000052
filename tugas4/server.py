import logging
import socket
import sys
import threading
import time
from datetime import datetime
from struct import pack, unpack
from typing import Optional

from deps.config import Config
from deps.utils import Action, Packet
from deps.parser import Mode, Parser

config = Config()

parser = Parser(Mode.Server)
parser.parse()

config.from_args(parser)


class FileConnHandler(threading.Thread):
    def __init__(self, fname: str, mode: Action, *, conn: Optional[socket.socket] = None, port: Optional[int] = 0):
        self.conn: socket.socket = conn if conn else socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.bind((config.config["host"], port))
        self.fname = fname
        self.port = port
        self.mode = mode
        super().__init__()

    def send(self, conn: socket.socket):
        logging.info(f"Sending file {self.fname} to client")
        with open(f'{config.config["dir"]}/{self.fname}', 'rb') as f:
            conn.sendfile(f)
            conn.shutdown(socket.SHUT_WR)
    
    def recv(self, conn: socket.socket):
        with open(f'{config.config["dir"]}/{self.fname}', 'wb+') as f:
            while True:
                data = conn.recv(Packet.BUFFER)
                f.write(data)
                if not data:
                    break

    def run(self):
        self.conn.listen()
        while True:
            serv, addr = self.conn.accept()

            logging.info(f"Connection from {addr}")
            logging.info(f"Acting as fileserver at {self.port}")

            if(self.mode == Action.POST):
                self.recv(serv)
            elif(self.mode == Action.GET):
                self.send(serv)


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

    def vacant_sock(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:  # create TCP/IP socket
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            sock.bind((config.config["host"], 0))
            addr = sock.getsockname()
            logging.info(f"Will use {addr} as address for sending file")

        return addr

    def run(self):
        while True:
            req = self.recv()
            logging.info(f"Action received as {req.cmd}")
            if req and req.cmd:
                if Action[req.cmd] == Action.LIST:
                    packet = Packet(req.cmd, config.config["dir"])
                    self.send(packet.result)
                    break
                elif Action[req.cmd] in [Action.POST, Action.GET]:
                    addr = self.vacant_sock()
                    
                    file_client = FileConnHandler(req.data, mode=Action[req.cmd], port=addr[1])
                    file_client.start()
                    packet = Packet(req.cmd, addr[1])
                    self.send(packet.result)
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
            print()
            logging.info(f"Connection from {addr}")

            client = ClientHandler(conn, addr)
            client.start()
            self.clients.append(client)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    Server().start()