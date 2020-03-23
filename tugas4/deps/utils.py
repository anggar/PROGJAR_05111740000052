import json
import os
from enum import Enum
from typing import Optional

class Packet:
    BUFFER = 1024

    def __init__(self, cmd="", arg="", part: Optional[bytes] = None):
        self.cmd = cmd
        self.data = arg
        self.part = part

    def __repr__(self):
        return {"cmd": self.cmd, "data": self.data}

    def __str__(self):
        return str(self.__repr__())

    @property
    def result(self):
        if Action[self.cmd] == Action.LIST:
            self.cmd = "result"
            self.data = str(os.listdir())
        if Action[self.cmd] == Action.POST:
            with open(self.data, 'ab+') as f:
                f.write(self.part)

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