from GraphTools import *
import json
from IO_Azure import *
import re



graphMenu = {"1":("Salt ultrasonic level graph",levelGraph),
        "2":("Temperature graph",tempGraph),
       }
print("Which type of graph do you want to save?")
for key in sorted(graphMenu.keys()):
     print(key+": " + graphMenu[key][0])
graphAns = input("Please type in a digit.")
if not re.match("\d", graphAns):
    raise ValueError("User input must be a number")

print("Which date do you want to get data on?")

dateAns = input("Please type in a date in YYYY-MM-DD format.")
if not re.match("\d\d\d\d-\d\d-\d\d", dateAns):
    raise ValueError("Date was not in specified format")

if graphAns == "1":
    dict = readDayAzureLevelDict(dateAns)
else:
    dict = readDayAzureTempDict(dateAns)



fileName = graphMenu[graphAns][1](dict, dateAns)
print(fileName + " was saved")
