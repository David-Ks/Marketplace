import base64
import hashlib


def encodeToMd5(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


def encodeToBase64(string):
    return base64.b64encode(bytes(str(string), "utf-8")).decode("utf-8")
