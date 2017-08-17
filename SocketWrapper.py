import re

class SocketRadar(object):
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
    socket = SocketRadar()
    socket.sock = sock
    socket.ip = ip
    socket.port = port
    socket.id = 'r' + re.match(".*\.(\d\d)", ip).group(1) + 'p' + re.match("\d\d\d(\d\d)", str(port)).group(1)
    socket.dict = {"deviceID": socket.id, "Blocks": []}
    return socket

class SocketTemp(object):
    def __init__(self):
        self.newBlock = True
        self.dict = {}
        self.block = []
        self.sock = None
        self.ip = ''
        self.port = 0

    def resetData(self):
        self.newBlock = True
        self.dict = {"deviceID": "old-tp01p01", "Blocks": []}
        self.block = []

def make_socket_temp(sock, ip, port):
    socket = SocketTemp()
    socket.sock = sock
    socket.ip = ip
    socket.port = port
    socket.dict = {"deviceID": "old-tp01p01", "Blocks": []}
    return socket

class SocketLevel(object):
    def __init__(self):
        self.newBlock = True
        self.dict = {}
        self.block = []
        self.sock = None
        self.ip = ''
        self.port = 0

    def resetData(self):
        self.newBlock = True
        self.dict = {"deviceID": "old-lvl01p02", "Blocks": []}
        self.block = []

def make_socket_level(sock, ip, port):
    socket = SocketLevel()
    socket.sock = sock
    socket.ip = ip
    socket.port = port
    socket.dict = {"deviceID": "old-lvl01p02", "Blocks": []}
    return socket

class SocketRFIDLog(object):
    def __init__(self):
        self.newBlock = True
        self.dict = {}
        self.block = []
        self.sock = None
        self.ip = ''
        self.port = 0

    def resetData(self):
        self.newBlock = True
        self.dict = {"deviceID": "rf-l70p01", "Blocks": []}
        self.block = []

def make_socket_rfid_log(sock, ip, port):
    socket = SocketRFIDLog()
    socket.sock = sock
    socket.ip = ip
    socket.port = port
    socket.dict = {"deviceID": "rf-l70p01", "Blocks": []}
    return socket

class SocketRFIDState(object):
    def __init__(self):
        self.newBlock = True
        self.dict = {}
        self.block = []
        self.sock = None
        self.ip = ''
        self.port = 0

    def resetData(self):
        self.newBlock = True
        self.dict = {"deviceID": "rf-s70p01", "Blocks": []}
        self.block = []

def make_socket_rfid_state(sock, ip, port):
    socket = SocketRFIDState()
    socket.sock = sock
    socket.ip = ip
    socket.port = port
    socket.dict = {"deviceID": "rf-s70p01", "Blocks": []}
    return socket