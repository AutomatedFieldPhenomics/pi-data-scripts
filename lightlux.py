#!/usr/bin/python3

from python_tsl2591 import tsl2591
import os
import datetime
import csv

csvFile = '/home/pi1/sensorData/lightlux3.csv'
dir = '/home/pi1/sensorData'

def initialize():
    sensor = tsl2591()
    sensor.set_timing(0x03)
    return sensor

def recordLux(lux, full, ir):
    # Get current time
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M")

    # Make directory
    if not os.path.exists(dir):
        os.makedirs(dir)

    # Create CSV file
    firstRow = "Lux, Full, IR, Date (ymd), Time\n"
    if not os.access(csvFile, os.F_OK):
        with open(csvFile, 'a') as fd:
            fd.write(firstRow)

    # Record data
    currentRow = '{L},{F},{I},{D},{t}\n'.format(L=lux, F=full, I=ir, D=date, t=time)
    with open(csvFile, 'a') as fd:
        fd.write(currentRow)

def adjustSensor(sensor):
    data = sensor.get_current()
    full = data['full']
    lux = data['lux']
    gain = sensor.get_gain()
    prevGain = gain
    timing = sensor.get_timing()

    print(sensor.get_current())
    while ((full < 16383 or full  > 49151) and (gain != 0x00 or timing != 1) and (gain != 0x30 or timing != 5) and 
            (timing != 5 or prevGain <= gain) and (timing != 1 or prevGain >= gain)):
        if(full < 16383):
            if(timing == 5):
                prevGain = gain
                gain = gain + 0x10
                sensor.set_gain(gain)
                sensor.set_timing(3)
            else:
                sensor.set_timing(timing + 1)

        elif(full > 49151):
            if(timing == 1):
                prevGain = gain
                gain = gain - 0x10
                sensor.set_gain(gain)
                sensor.set_timing(3)
            else:
                sensor.set_timing(timing - 1)
        
        data = sensor.get_current()
        lux = data['lux']
        full = data['full']
        timing = sensor.get_timing()
        print(sensor.get_current())

def main():
    sensor = initialize()
    adjustSensor(sensor)
   
    full, ir = sensor.get_full_luminosity()
    lux = sensor.calculate_lux(full, ir)

    recordLux(lux, full, ir)

if __name__ == "__main__":
    main()
