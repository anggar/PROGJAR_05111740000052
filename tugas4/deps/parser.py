import argparse
from enum import Enum
from typing import Dict, Union

ArgsType = Dict[str, Union[str, int]]


class Mode(Enum):
    Client = 0
    Server = 1


class Parser:
    nargs_server : ArgsType = {"cmd": '?', "arg": '?'}
    nargs_client : ArgsType = {"cmd": 1, "arg": '*'}

    def __init__(self, mode: Mode):
        nargs_val : ArgsType = self.nargs_server if mode == Mode.Server else self.nargs_client
        
        self.parser = argparse.ArgumentParser(description="Fileserver using socket and thread")
        self.parser.add_argument(
            'cmd', metavar='cmd', type=str, nargs=nargs_val["cmd"],
            help='Command that will fed to system'
        )
        self.parser.add_argument(
            'arg', metavar='arg', type=str, nargs=nargs_val["arg"],
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
        self.args : ArgsType = {}
    
    def parse(self):
        self.args = self.parser.parse_args()

    @property
    def host(self):
        return self.args.host

    @property
    def port(self):
        return self.args.port
