import base64

class Encoding:
    def string(string: str) -> str:
        return base64.b64encode(string.encode('utf-8'))