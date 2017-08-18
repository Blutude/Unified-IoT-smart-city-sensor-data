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

def vdmFormatDict():
    dict = {"Format":"ODNF1", "Desc":"", "CreateUtc":"",
            "ExpireUtc": "0000-00-00T00:00:00", "Unit":"", "Status":"", "Value": ""}
    return dict

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

        if out.startswith("$RDTGT"):
            if len(out) > 6: # Target not empty
                dateTimeStamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                t = out.split(',')
                targets = []
                for i in range(1, len(t), 3):
                    target = make_target(t[i], t[i + 1], t[i + 2])
                    targets.append(target)
                for tgt in targets:
                    dict = vdmFormatDict()
                    dict["Desc"] = "Detected target report"
                    dict["CreateUtc"] = dateTimeStamp
                    dict["Unit"] = "object"
                    if tgt.D == "1":
                        dir = "Approaching"
                    else:
                        dir = "Receding"
                    dict["Value"] = {"Direction": dir, "Speed": tgt.S, "Detection level": tgt.L}
                    mySocket.dict["Blocks"].extend(dict)

        elif out.startswith("$RDSTA"):
            s = out.split(',')
            dateTimeStamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            dict = vdmFormatDict()
            dict["Desc"] = "Approaching target statistics report"
            dict["CreateUtc"] = dateTimeStamp
            dict["Unit"] = "object"
            dict["Value"] = {{"Timeslot counter": s[1], "Average speed": s[2], "Min speed": s[3], "Max speed": s[4], "Road occupation percentage": s[5],
                      "Temporary counter": s[6]}}
            mySocket.dict["Blocks"].extend(dict)

        elif out.startswith("$RDSTR"):
            s = out.split(',')
            dateTimeStamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            dict = vdmFormatDict()
            dict["Desc"] = "Receding target statistics report"
            dict["CreateUtc"] = dateTimeStamp
            dict["Unit"] = "object"
            dict["Value"] = {{"Timeslot counter": s[1], "Average speed": s[2], "Min speed": s[3], "Max speed": s[4],
                              "Road occupation percentage": s[5],
                              "Temporary counter": s[6]}}
            mySocket.dict["Blocks"].extend(dict)

        elif out.startswith("$RDCNT"):
            s = out.split(',')
            dateTimeStamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            dict = vdmFormatDict()
            dict["Desc"] = "Targets count report"
            dict["CreateUtc"] = dateTimeStamp
            dict["Unit"] = "object"
            dict["Value"] = {"Direction": s[1], "Speed": s[2], "Detection level": s[3], "Cumulative counter for approaching targets": s[4],
                              "Cumulative counter for receding targets": s[5]}
            mySocket.dict["Blocks"].extend(dict)

        else:
            raise ValueError("Missed a type of report?")

        if sys.getsizeof(_pickle.dumps(mySocket.dict)) > Constants.FILE_SIZE_LIMIT:
            break

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

    try:
        uid,time,antennaNb = readRFIDSocket(mySocket.sock, freshStart)
    except ConnectionResetError:
        print("Connection to socket was forcibly closed by the remote host.")
        return True

    dateTimeStamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    dict = vdmFormatDict()
    dict["Desc"] = "RFID scan"
    dict["CreateUtc"] = dateTimeStamp
    dict["Unit"] = "object"
    dict["Status"] = "bad" # time is not valid - issue
    dict["Value"] = {"UID": uid, "Time": time, "Antenna number": antennaNb}
    mySocket.dict["Blocks"].extend(dict)

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

    dateTimeStamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    uidFound = False
    for block in mySocket.dict["Blocks"]:
        value = block["Value"]
        if value["UID"] == uid:
            uidFound = True
            if value["State"] == "0":
                value["State"] = "1"
            else:
                value["State"] = "0"

    if not uidFound:
        dict = vdmFormatDict()
        dict["Desc"] = "UID state"
        dict["CreateUtc"] = dateTimeStamp
        dict["Unit"] = "object"
        dict["Status"] = ""
        dict["Value"] = {"UID": uid, "State": "0"}
        mySocket.dict["Blocks"].extend(dict)

    print("uid: " + uid + " - time: " + myTime + " - antenna#: " + antennaNb)

    return False # no socket timed out so return False

def resetUidStates(mySocket):
    for block in mySocket.dict["Blocks"]:
        block["Value"]["State"] = "0"