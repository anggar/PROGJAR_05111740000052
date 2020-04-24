from typing import Dict, List

class Request:
    def __init__(self):
        self.address: str = ""
        self.method: str = ""
        self.headers: Dict[str, str] = {}
        self.body: str = ""

    def load_header(self, raw: str) -> None:
        req = raw.split("\r\n")
        spl = req[0].split(" ")
        self.method = spl[0]
        self.address = spl[1]

        headers = [n for n in req[1:] if n != '']
        for h in headers:
            hr = h.split(":", 1)
            self.headers[hr[0].lower()] = hr[1]

    def load_body(self, raw: str) -> None:
        self.body = raw.split("=")[1] if raw else ""

    @property
    def headers_list(self) -> List[str]:
        ret: List[str] = []
        for i in self.headers:
            ret += [f"<strong>{i}</strong>: {self.headers[i]}"]
        return ret
