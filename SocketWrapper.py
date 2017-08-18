import re

class Socket:
    def __init__(self, sock, ip, port):
        self.dict = {}
        self.sock = sock
        self.ip = ip
        self.port = port

class SocketRadar(object):
    def __init__(self, sock, ip, port):
        Socket.__init__(self, sock, ip, port)
        self.id = 'r' + re.match(".*\.(\d\d)", ip).group(1) + 'p' + re.match("\d\d\d(\d\d)", str(port)).group(1)
        self.dict = {"deviceID": self.id, "Blocks": []}

    def resetData(self):
        self.dict = {"deviceID": self.id, "Blocks": []}

class SocketRFIDLog(object):
    def __init__(self, sock, ip, port):
        Socket.__init__(self, sock, ip, port)
        self.dict = {"deviceID": "rf-l70p01", "Blocks": []}

    def resetData(self):
        self.dict = {"deviceID": "rf-l70p01", "Blocks": []}

class SocketRFIDState(object):
    def __init__(self, sock, ip, port):
        Socket.__init__(self, sock, ip, port)
        self.dict = {"deviceID": "rf-s70p01", "Blocks": []}

    def resetData(self):
        self.dict = {"deviceID": "rf-s70p01", "Blocks": []}