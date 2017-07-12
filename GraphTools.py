import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

def speedHistogram(dict, date, deviceID):
    speeds = [0,0,0,0,0,0,0,0,0,0,0,0,0] # 0-10, 10-20, 20-30, ..., 110-120, 120+

    for block in dict:
        if block["Counting"]:
            if re.match("{}.*".format(date), block["StartDateTime"]):
                for vehicle in block["Counting"]:
                    speed = float(vehicle["RDCNT"]["S"])
                    if speed < 10:
                        speeds[0]+=1
                    elif speed < 20:
                        speeds[1]+=1
                    elif speed < 30:
                        speeds[2]+=1
                    elif speed < 40:
                        speeds[3]+=1
                    elif speed < 50:
                        speeds[4]+=1
                    elif speed < 60:
                        speeds[5]+=1
                    elif speed < 70:
                        speeds[6]+=1
                    elif speed < 80:
                        speeds[7]+=1
                    elif speed < 90:
                        speeds[8]+=1
                    elif speed < 100:
                        speeds[9]+=1
                    elif speed < 110:
                        speeds[10]+=1
                    elif speed < 120:
                        speeds[11]+=1
                    else:
                        speeds[12]+=1

    y = pd.Series.from_array(speeds)
    my_xticks = ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100', '100-110', '110-120', '120+']
    plt.figure(figsize=(20, 10))
    ax = y.plot(kind='bar')
    ax.set_title("Speed Histogram - {}".format(date))
    ax.set_xlabel("Speed (km/h)")
    ax.set_ylabel("Number of vehicles")
    ax.set_xticklabels(my_xticks, rotation='horizontal')

    rects = ax.patches

    for rect, label in zip(rects, speeds):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2, height + 5, label, ha='center', va='bottom')

    fileName = 'speed-' + deviceID + '.png'
    plt.savefig(fileName)
    return fileName


def timeOfDayHistogram(dict, date, deviceID):
    approachingHours = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    recedingHours = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    for block in dict:
        if block["Counting"]:
            if re.match("{}.*".format(date), block["StartDateTime"]):
                for vehicle in block["Counting"]:
                    if int(vehicle["RDCNT"]["D"]) == 1:
                        datetime = vehicle["RDCNT"]["datetime"]
                        hour = int(re.match(".* (\d*):.*", datetime).group(1))
                        approachingHours[hour] += 1
                    elif int(vehicle["RDCNT"]["D"]) == -1:
                        datetime = vehicle["RDCNT"]["datetime"]
                        hour = int(re.match(".* (\d*):.*", datetime).group(1))
                        recedingHours[hour] += 1
                    else:
                        raise ValueError("D can't be something other than 1 or -1. Investigate.")

    x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23])
    y1 = np.array(approachingHours)
    y2 = np.array(recedingHours)
    plt.figure(figsize=(20, 10))
    plt.title("Time of Day Histogram - {}".format(date))
    plt.xlabel("Hour of the day")
    plt.ylabel("Number of vehicles")
    plt.xticks(x)
    #plt.yticks(np.arange(0, y1.max() + y2.max(), 1))
    p1 = plt.bar(x, y1, color='#d62728')
    p2 = plt.bar(x, y2, bottom=y1)
    plt.legend((p1[0], p2[0]), ('Approaching vehicles', 'Receding vehicles'))
    fileName = 'timeOfDay-' + deviceID+ '.png'
    plt.savefig(fileName)
    return fileName