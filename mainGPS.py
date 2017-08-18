import socket
from Parsing import *
from IO_Azure import *
import time
import re
import datetime
import getpass
import sys
import telnetlib
from Parsing import vdmFormatDict


if __name__ == "__main__":
    HOST = ''  # Symbolic name, meaning all available interfaces
    PORT = 22335  # Arbitrary non-privileged port

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('Socket created')

    # Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()

    print('Socket bind complete')

    # Start listening on socket
    #s.listen(10)
    #print('Socket now listening')

    # now keep talking with the client
    # wait to accept a connection - blocking call
    while True:
        try:
            data, addr = s.recvfrom(1024)
            dateTimeStamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            print(str(data))
            doc, doc_link = readAzureGPSDict()
            data = re.match(".*\$GPGGA(.*)\*.*\*", str(data)).group(1)
            data = data.split(',')
            time = data[1]
            latitude = data[2] + ',' + data[3]
            longitude = data[4] + ',' + data[5]
            fixQuality = data[6]
            satellitesNb = data[7]
            horizontalDilution = data[8]
            altitude = data[9] + ',' + data[10]
            heightOfGeoID = data[11] + ',' + data[12]

            dict = vdmFormatDict()
            dict["Desc"] = "GPS fix data"
            dict["CreateUtc"] = dateTimeStamp
            dict["Unit"] = "object"
            dict["Value"] = {"TimeStamp": str(time), "Latitude": str(latitude), "Longitude": str(longitude)}

            print(dict)
            doc["Blocks"].extend(dict)

            replaceAzureDict(doc, doc_link)
        except Exception as e:
            print(str(e))
    s.close()