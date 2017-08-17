import socket
from IO_Azure import *
import time
import re
import datetime
import sys

if __name__ == "__main__":
    HOST = ''  # Symbolic name, meaning all available interfaces
    PORT = 10001  # Arbitrary non-privileged port

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    # Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()

    print('Socket bind complete')

    # Start listening on socket
    s.listen(10)
    print('Socket now listening')

    # now keep talking with the client
    # wait to accept a connection - blocking call
    while 1:
        print("test4")
        conn, addr = s.accept()
        print("test5")
        conn.settimeout(15)
        try:
            print('Connected with ' + addr[0] + ':' + str(addr[1]))
            t = 't'
            regexPattern = ".*Air Temp (\d+) C.*Road Temp (\d+).*"
            regexBadFormatPattern = ".*%Q.*"
            while 1:
                start = time.time()
                dict, doc_link = readAzureTempDict()
                regexMatch = ""
                regexBadFormatMatch = ""
                while not regexMatch:
                    conn.send(t.encode())
                    data = conn.recv(50)
                    print(data)
                    regexMatch = re.match(regexPattern, str(data))
                    regexBadFormatMatch = re.match(regexBadFormatPattern, str(data))
                    if regexBadFormatMatch:
                        conn.send(bytes.fromhex('0323'))
                airTemp = regexMatch.group(1)
                roadTemp = regexMatch.group(2)
                dateTimeStamp = datetime.datetime.now()
                block = {"Air Temp": airTemp, "Road Temp": roadTemp, "datetime": dateTimeStamp.strftime("%Y-%m-%dT%H:%M:%S")}
                for x in block:
                    print(x+": "+block[x])
                dict["Blocks"].append(block)
                replaceAzureDict(dict, doc_link)
                while time.time() - start < 900: # get data every 15 minutes = 900 seconds
                    pass
        except Exception as e: # goes back to accepting a connection phase
            print("test1")
            print(str(e))
            print("test2")
        print("test3")
    s.close()