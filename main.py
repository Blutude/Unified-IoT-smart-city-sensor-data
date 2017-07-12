from Parsing import *
from IO_Azure import *
import serial
import sys
import os
import socket
from SocketWrapper import make_socket_radar
import multiprocessing
import datetime


def setup(address, port):
    connected = False
    freshDisconnection = True
    while True:
        if not connected:
            mySocket = connection(address, port, freshDisconnection)

        freshDisconnection = True
        connected = True
        interrupted = extract(mySocket)
        if interrupted:
            connected = False
            freshDisconnection = False # prevents connection method from rewriting the same timeout
            writeTimeouts(mySocket.dict, mySocket.id, datetime.datetime.now())
        if mySocket.dict["Blocks"] or interrupted or mySocket.dict["Timeouts"]:
            writeAzure(mySocket.dict)
        mySocket.resetData() # Clear data for next iteration


def connection(address, port, freshDisconnection): # only write timeouts if it just timed out. Not if it stays timed out.
    isConnected = False
    disconnected_date_time = None
    while not isConnected:
        sock = socket.socket()
        sock.settimeout(5)
        try:
            sock.connect((address, port))
        except socket.timeout:
            if freshDisconnection:
                freshDisconnection = False
                print("Sock: ({},{}) not connected".format(address, port))
                disconnected_date_time = datetime.datetime.now()
            continue

        isConnected = True

    mySocket = make_socket_radar(sock, address, port)
    print("Sock: ({},{}) connected".format(address, port))
    if disconnected_date_time:
        writeTimeouts(mySocket.dict, mySocket.id, disconnected_date_time)
    return mySocket


if __name__ == "__main__":
    p = 10001
    for a in Constants.ADDRESSES:
        for j in range(0, 2):
            pro = multiprocessing.Process(target=setup, args=(a, p,))
            pro.start()
            if p == 10001:
                p += 1
            else:
                p -= 1

