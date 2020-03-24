import logging
import socket
from typing import Optional

from deps.config import Config
from deps.utils import Action, Packet
from deps.parser import Mode, Parser


config = Config()

parser = Parser(Mode.Client)
parser.parse()

config.from_args(parser)

class Client:
    def __init__(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = (config.config["host"], config.config["port"])
        logging.info(f"Connecting to {addr}")
        try:
            self.conn.connect(addr)
        except ConnectionRefusedError:
            logging.error(f"Connection to {addr} refused. Aborting.")
            exit()

    def send(self, packet: Packet) -> None:
        logging.info(f"Sending request packet")
        self.conn.sendall(packet.json.encode())
        self.conn.shutdown(socket.SHUT_WR)

    def recv(self) -> Optional[Packet]:
        data = b''
        while True:
            data_rcv = self.conn.recv(Packet.BUFFER)
            if not data_rcv:
                break
            data += data_rcv
        try:
            packet = Packet().from_json(data.decode())
            return packet
        except Exception as e:
            logging.error(f'recv client: {e}')
            return None

    def handlefile(self, conn: socket.socket, fname: str, mode: Action):
        if mode == Action.POST:
            with open(fname, 'rb') as f:
                conn.sendfile(f)
                conn.shutdown(socket.SHUT_RD)
        elif mode == Action.GET:
            logging.info(f"Receiving data from {conn.getsockname()}")
            with open(fname, 'wb') as f:
                while True:
                    data = conn.recv(Packet.BUFFER)
                    f.write(data)
                    if data == b'':
                        break

    def action(self, cmd, arg):
        cmd = cmd[0].upper() if cmd else ''
        arg = arg[0] if arg else ''

        if Action[cmd] in [Action.LIST, Action.POST, Action.GET]:
            packet = Packet(cmd, arg)
            self.send(packet)
            res = self.recv()
            if res.cmd == 'result':
                print(f"Result:\n {res.data}")
            elif res.cmd == 'port':
                logging.info(f"Will be connecting to socket port: {res.data}")

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:  # create TCP/IP socket
                    sock.connect((config.config["host"], res.data))
                    logging.info(f"Make {cmd} action with file {arg}")
                    self.handlefile(sock, arg, Action[cmd])


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    client = Client()
    client.action(parser.args.cmd, parser.args.arg)
