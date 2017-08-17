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

def readRadarSocket(sock):
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

def extractRadar(mySocket): # returns true if was interrupted
    if not mySocket:
        return False

    sizeLimit = False
    while True:
        try:
            out = readRadarSocket(mySocket.sock)
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


    #with open('test' + mySocket.id + '.json', 'w') as f:
        #json.dump(mySocket.dict, f, sort_keys=True, indent=4)  # , default=json_util.default)
    return False # no socket timed out so return False


def writeTimeouts(dict, socketID, date_time):
    if "Timeouts" in dict:
        dict["Timeouts"].append({"DateTime": date_time.strftime("%Y-%m-%d %H:%M:%S"), "deviceID":socketID})
    else:
        dict.update({"Timeouts":[{"DateTime": date_time.strftime("%Y-%m-%d %H:%M:%S"), "deviceID":socketID}]})



def readRFIDSocket(sock, freshStart):
    out = ''
    char = str(sock.recv(1))[2]
    if freshStart: # skip first sentence to make sure we start reading the sentence from the beginning
        while not char.__eq__('\\'):
            char = str(sock.recv(1))[2]
        char = str(sock.recv(1))[2]
        char = str(sock.recv(1))[2]
    while not char.__eq__('\\'):
        out += char
        b = str(sock.recv(1))
        char = b[2]
    char = str(sock.recv(1))[2] # to get to the end of the sentence and get buffer ready for new sentence
    s = out.split(",")
    if len(s) != 3:
        raise ValueError("Investigate")
    return (s[0], s[1], s[2])

def extractRFIDLog(mySocket, freshStart): # returns true if was interrupted
    if not mySocket:
        return True

    sizeLimit = False

    try:
        uid,time,antennaNb = readRFIDSocket(mySocket.sock, freshStart)
    except ConnectionResetError:
        print("Connection to socket was forcibly closed by the remote host.")
        return True

    mySocket.dict["Blocks"].append({"uid": uid, "time": time, "antennaNb": antennaNb})

    print("uid: " + uid + " - time: " + time + " - antenna#: " + antennaNb)



    with open('test.json', 'w') as f:
        json.dump(mySocket.dict, f, sort_keys=True, indent=4)  # , default=json_util.default)
    return False # no socket timed out so return False

def extractRFIDState(mySocket, freshStart): # returns true if was interrupted
    if not mySocket:
        return True

    #start = time.time()
    #while time.time() - start < 25: # uploads every 25 seconds
    try:
        uid,myTime,antennaNb = readRFIDSocket(mySocket.sock, freshStart)
    except ConnectionResetError:
        print("Connection to socket was forcible closed by the remote host.")
        return True

    uidFound = False
    for block in mySocket.dict["Blocks"]:
        if block["uid"] == uid:
            uidFound = True
            if block["state"] == "0":
                block["state"] = "1"
            else:
                block["state"] = "0"

    if not uidFound:
        mySocket.dict["Blocks"].append({"uid": uid, "state":"0"})

    print("uid: " + uid + " - time: " + myTime + " - antenna#: " + antennaNb)

    return False # no socket timed out so return False

def resetUidStates(mySocket):
    for block in mySocket.dict["Blocks"]:
        block["state"] = "0"