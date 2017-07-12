import serial
from Target import *
import re
import json
import datetime
import sys
#from bson import json_util
import _pickle
from socket import timeout
from Constants import Constants

def readSocket(sock):
    out = ''
    char = str(sock.recv(1))[2]
    while not char.__eq__('$'):
        char = str(sock.recv(1))[2]
    while not char.__eq__('\\'):
        out += char
        b = str(sock.recv(1))
        char = b[2]
    char += str(sock.recv(1))[2]
    if not char.__eq__('\\\\'):
        raise ValueError("Investigate")
    return out

def extract(mySocket): # returns true if was interrupted
    if not mySocket:
        return False

    sizeLimit = False
    while True:
        try:
            out = readSocket(mySocket.sock)
        except timeout:
            print("socket " + mySocket.id + " timed out.")
            return True
        except ConnectionResetError:
            print("Connection to socket " + mySocket.id + " was forcibly closed by the remote host.")
            return True
        out = re.match(".*(\$.*)\*.*", out).group(1)

        print("Sock: ({},{}), Msg: {}".format(mySocket.ip, mySocket.port, out))

        if mySocket.newBlock:
            mySocket.dict["Blocks"].extend(mySocket.block)
            mySocket.block = [
                {"StartDateTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Counting": [], "Targets": [],
                 "RDSTA": {}, "RDSTR": {}, "EndDateTime": None}]
            mySocket.newBlock = False

        if out.startswith("$RDTGT"):
            if len(out) > 6: # Target not empty
                t = out.split(',')
                targets = []
                for i in range(1, len(t), 3):
                    target = make_target(t[i], t[i + 1], t[i + 2])
                    targets.append(target)
                d = [{"RDTGT": {"datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}}]
                i = 1
                for tgt in targets:
                    d[0]["RDTGT"].update({"D" + str(i): tgt.D, "S" + str(i): tgt.S, "L" + str(i): tgt.L})
                    i += 1
                    mySocket.block[0]["Targets"].extend(d)

        elif out.startswith("$RDSTA"):
            s = out.split(',')
            d = {"datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            d.update({"count": s[1], "avgSpeed": s[2], "minSpeed": s[3], "maxSpeed": s[4], "roadOCP": s[5],
                      "tmpCNT": s[6]})#re.match("(.*)\*.*", s[6]).group(1)})
            mySocket.block[0]["RDSTA"].update(d)

        elif out.startswith("$RDSTR"):
            s = out.split(',')
            d = {"datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            d.update({"count": s[1], "avgSpeed": s[2], "minSpeed": s[3], "maxSpeed": s[4], "roadOCP": s[5],
                      "tmpCNT": s[6]})#re.match("(.*)\*.*", s[6]).group(1)})
            mySocket.block[0]["RDSTR"].update(d)
            mySocket.block[0]["EndDateTime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if sizeLimit:
                mySocket.dict["Blocks"].extend(mySocket.block)
                break
            mySocket.newBlock = True

        elif out.startswith("$RDCNT"):
            s = out.split(',')
            d = [{"RDCNT": {"datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}}]
            d[0]["RDCNT"].update({"D": s[1], "S": s[2], "L": s[3], "aprCNT": s[4],
                                  "rcdCNT": s[5]})#re.match("(.*)\*.*", s[5]).group(1)})
            mySocket.block[0]["Counting"].extend(d)

        else:
            raise ValueError("Missed a type of report?")

        if sys.getsizeof(_pickle.dumps(mySocket.dict)) > Constants.FILE_SIZE_LIMIT:
            sizeLimit = True


    with open('test' + mySocket.id + '.json', 'w') as f:
        json.dump(mySocket.dict, f, sort_keys=True, indent=4)  # , default=json_util.default)
    return False # no socket timed out so return False


def writeTimeouts(dict, socketID, date_time):
    if "Timeouts" in dict:
        dict["Timeouts"].append({"DateTime": date_time.strftime("%Y-%m-%d %H:%M:%S"), "deviceID":socketID})
    else:
        dict.update({"Timeouts":[{"DateTime": date_time.strftime("%Y-%m-%d %H:%M:%S"), "deviceID":socketID}]})
