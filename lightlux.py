#!/usr/bin/env python3

# Records light levels with tsl2591 lux sensor

from python_tsl2591 import tsl2591
import os
import datetime
import csv

# Append data to CSV
currentRow = "{L},{F},{I},{D},{t}\n".format(L=lux, F=full, I=ir, D=date, t=time)
with open(path, 'a') as fd:
    fd.write(currentRow)

def getLux():
    tsl = tsl2591()
    full, ir = tsl.get_full_luminosity()
    lux = tsl.calculate_lux(full, ir)
    return lux

def getFile(now):
    csvFile = now.strftime("%Y-%m") + ".csv"
    dir = '/home/pi/sensorData/tsl2591'
    path = dir + '/' + csvFile

    # Create directory if it doesn't exist
    if not os.path.exists(dir):
        os.makedirs(dir)

    # Create csv file if one doesn't exist
    firstRow = 'Lux, Full, IR, Date (ymd), Time\n'
    if not os.access(path, os.F_OK):
        with open(path, 'a') as fd:
            fd.write(firstRow)

    return path

def recordLux(lux, path):
    current

def main():
    now = datetime.datetime.now()
    lux = getLux()
    path = getFile(now)



if __name__ == "__main__":
    main()
