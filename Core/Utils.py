from json import loads
from base64 import b64decode

class Utils:
    @staticmethod
    def base64_decode(data):
        padding = len(data) % 4
        if padding:
            data += '=' * (4 - padding)
        return b64decode(data).decode('utf-8')