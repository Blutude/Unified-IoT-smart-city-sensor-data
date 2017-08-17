from GraphTools import *
import json
from IO_Azure import *
import re


#with open('radar2.json', 'r') as f:
    #dict = json.load(f)

#### GRAPH INPUT
graphMenu = {"1":("Speed Histogram",speedHistogram),
        "2":("Time Of Day Histogram",timeOfDayHistogram)
       }
print("Which type of graph do you want to save?")
for key in sorted(graphMenu.keys()):
     print(key+": " + graphMenu[key][0])

graphAns = input("Please type in a digit.")
if not re.match("\d", graphAns):
    raise ValueError("User input must be a number")

#### RADAR INPUT
radarMenu = {"1":"r51p01",
        "2":"r51p02",
        "3":"r52p01",
        "4":"r52p02",
        "5":"r53p01",
        "6":"r53p02",
       }
print("Which radar do you want to get data on?")
for key in sorted(radarMenu.keys()):
     print(key+": " + radarMenu[key])

radarAns = input("Please type in a digit.")
if not re.match("\d", radarAns):
    raise ValueError("User input must be a number")

#### DATE INPUT
print("Which date do you want to get data on?")

dateAns = input("Please type in a date in YYYY-MM-DD format.")
if not re.match("\d\d\d\d-\d\d-\d\d", dateAns):
    raise ValueError("Date was not in specified format")

# CALLING GRAPH FUNCTION
radarID = radarMenu[radarAns]
dict = readDayAzureRadars(radarID, dateAns)
fileName = graphMenu[graphAns][1](dict, dateAns, radarID)
print(fileName + " was saved")
