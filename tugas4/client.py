import logging
import socket
import argparse
from typing import Optional

from deps.config import Config
from deps.utils import Action, Packet


config = Config()


class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Fileserver using socket and thread")
        self.parser.add_argument(
            'cmd', metavar='cmd', type=str, nargs=1,
            help='Command that will fed to system'
        )
        self.parser.add_argument(
            'arg', metavar='arg', type=str, nargs='*',
            help='Optional argument for command'
        )
        self.parser.add_argument(
            '--host', 
            dest='host', 
            action='store',
            help='specify host'
        )
        self.parser.add_argument(
            '--port', 
            dest='port', 
            action='store',
            help='specify port to use'    
        )
        self.args = {}
    
    def parse(self):
        self.args = self.parser.parse_args()


parser = Parser()
parser.parse()


class Client:
    def __init__(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = (config.config["host"], config.config["port"])
        logging.info(f"Connecting to {addr}")
        self.conn.connect(addr)

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

    def action(self, cmd, arg):
        cmd = cmd[0] if cmd else ''
        arg = arg[0] if arg else ''

        if Action[cmd.upper()] == Action.LIST:
            packet = Packet(cmd, arg)
            self.send(packet)
            res = self.recv()
            if res.cmd == 'result':
                print(f"Result:\n {res.data}")
        elif Action[cmd.upper()] == Action.POST:
            with open(arg, 'rb+') as f:
                for chunk in iter(lambda: f.read(Packet.BUFFER), b''):
                    packet = Packet(cmd, arg, chunk)
                    self.send(chunk)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    client = Client()
    client.action(parser.args.cmd, parser.args.arg)
