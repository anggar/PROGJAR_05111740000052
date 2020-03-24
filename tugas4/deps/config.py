import json
from typing import Optional

from .parser import Parser

class Config:
    def __init__(self, file="config.json"):
        self.file = file
        self.config = {"host": "", "port": 0}

        with open(self.file) as f:
            self.config = json.load(f)

        self.config["port"] = int(self.config["port"])

    def host(self, x: Optional[int] = None):
        self.config["host"] = x if x else self.config["host"]

    def port(self, x: Optional[int] = None):
        self.config["port"] = x if x else self.config["port"]

    def from_args(self, parser: Parser):
        self.config["host"] = \
            parser.args.host if parser.args.host else self.config["host"]

        self.config["port"] = \
            int(parser.args.port) if parser.args.port else self.config["port"]