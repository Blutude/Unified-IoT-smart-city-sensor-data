import re

class Socket(object):
    def __init__(self):
        self.newBlock = True
        self.dict = {}
        self.block = []
        self.sock = None
        self.ip = ''
        self.port = 0
        self.id = 0

    def resetData(self):
        self.newBlock = True
        self.dict = {"deviceID": self.id, "Blocks": []}
        self.block = []

def make_socket_radar(sock, ip, port):
    socket = Socket()
    socket.sock = sock
    socket.ip = ip
    socket.port = port
    socket.id = 'r' + re.match(".*\.(\d\d)", ip).group(1) + 'p' + re.match("\d\d\d(\d\d)", str(port)).group(1)
    socket.dict = {"deviceID": socket.id, "Blocks": []}
    return socket