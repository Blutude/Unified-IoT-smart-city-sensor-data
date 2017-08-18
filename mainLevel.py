import socket
from IO_Azure import *
import time
import datetime
import sys
from Parsing import vdmFormatDict

if __name__ == "__main__":
    HOST = ''  # Symbolic name, meaning all available interfaces
    PORT = 10002  # Arbitrary non-privileged port

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
    hex = '7e001310010013a20040e698d8fffe000001fb0503049e'
    while 1:
        print("test4")
        conn, addr = s.accept()
        print("test5")
        conn.settimeout(5)
        try:
            print('Connected with ' + addr[0] + ':' + str(addr[1]))
            while 1:
                start = time.time()
                conn.send(bytes.fromhex(hex))
                doc, doc_link = readAzureLevelDict()
                regexMatch = ""
                out = []
                try:
                    data = conn.recv(1)
                    while data:
                        out.append(data)
                        data = conn.recv(1)
                except socket.timeout:
                    pass
                print(out)
                if len(out) == 40:
                    dateTimeStamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                    range = out[-6:-4]
                    temperature = out[-4]
                    voltage = out[-3]

                    rangeValue = ord(range[1])*16**2+ord(range[0])
                    rangeValue /= 128
                    levelValue = 28 - rangeValue

                    temperatureValue = ord(temperature)
                    temperatureValue *= 0.587085
                    temperatureValue -= 50

                    voltageValue = ord(voltage)
                    voltageValue -= 14
                    voltageValue /= 40

                    dict = vdmFormatDict()
                    dict["Desc"] = "Ultrasonic level sensor data"
                    dict["CreateUtc"] = dateTimeStamp
                    dict["Unit"] = "object"
                    dict["Value"] = {"Level": str(levelValue), "Temperature": str(temperatureValue),
                             "Voltage": str(voltageValue)}

                    print(dict)
                    doc["Blocks"].extend(dict)

                    replaceAzureDict(doc, doc_link)
                    while time.time() - start < 900:  # get data every 15 minutes = 900 seconds
                        pass
                else:
                    with open("frames.txt", "a") as f:
                        for o in out:
                            f.write(str(o))
                        f.write("\r\n")
        except Exception as e:  # goes back to accepting a connection phase
            print("test1")
            print(str(e))
            print("test2")
    print("test3")
    s.close()