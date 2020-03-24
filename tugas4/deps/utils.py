import json
import os
import argparse
from enum import Enum
from typing import Optional

from .config import Config

config = Config()


class Packet:
    BUFFER = 1024

    def __init__(self, cmd="", arg=""):
        self.cmd = cmd
        self.data = arg

    def __repr__(self):
        return {"cmd": self.cmd, "data": self.data}

    def __str__(self):
        return str(self.__repr__())

    @property
    def result(self):
        if Action[self.cmd] == Action.LIST:
            self.cmd = "result"
            self.data = str(os.listdir(config.config["dir"]))
        elif Action[self.cmd] in [Action.POST, Action.GET]:
            self.cmd = "port"

        return self

    def from_json(self, data: str):
        jsoned = json.loads(data)
        self.cmd = jsoned["cmd"]
        self.data = jsoned["data"]

        return self

    @property
    def json(self):
        return json.dumps(self.__repr__())


class Action(Enum):
    LIST = 0
    POST = 1
    GET = 2