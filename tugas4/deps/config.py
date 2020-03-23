import json

class Config:
    def __init__(self, file="config.json"):
        self.file = file
        self.config = {"host": "", "port": 0}

        with open(self.file) as f:
            self.config = json.load(f)

        self.config["port"] = int(self.config["port"])