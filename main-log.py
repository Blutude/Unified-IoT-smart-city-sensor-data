import socket
from SocketWrapper import make_socket_rfid_log
from Parsing import *
from IO_Azure import *

def connection(address, port):
    isConnected = False
    while not isConnected:
        sock = socket.socket()
        #sock.settimeout(5)
        try:
            sock.connect((address, port))
        except socket.timeout:
            print("Sock: ({},{}) not connected".format(address, port))
            continue

        isConnected = True

    mySocket = make_socket_rfid_log(sock, address, port)
    print("Sock: ({},{}) connected".format(address, port))
    return mySocket


if __name__ == "__main__":
    address = "192.168.101.70"
    port = 10001

    freshStart = True # skip first sentence to make sure we start reading the sentence from the beginning
    connected = False
    while True:
        if not connected:
            mySocket = connection(address, port)
            freshStart = True

        connected = True
        mySocket.dict, doc_link = readAzureLogDict()
        interrupted = extractRFIDLog(mySocket, freshStart)
        freshStart = False
        if interrupted:
            connected = False
        replaceAzureDict(mySocket.dict, doc_link)
