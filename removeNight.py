#!/usr/bin/env python3

# This script removes all nighttime pictures from yesterday's image folder base on yesterday's sunrise and sunset

import json
import os
import datetime
from pathlib import Path

TWILIGHT = 0  # The approximate duration of twilight in minutes
              # When zero only images between sunrise and sunset will be kept

# Gets the sunrise and sunset times for the given date
def sunriseAndSet( date ):
    # Gets the weather JSON
    jsonFile = open("weather/" + date + "/23:00.json", 'r')
    data     = json.load(jsonFile)

    # Extract sunrise and sunset
    sys     = data['sys']
    sunrise = sys['sunrise']
    sunset  = sys['sunset']

    return sunrise,sunset

# Calculates the start and end of daylight before converting to local time
def convertLocal(sunrise, sunset, twilight):
    # Calculates start and end of daylight
    secTwlght = twilight * 60
    dayStart  = sunrise - secTwlght
    dayEnd    = sunset  + secTwlght

    # Converts to local time
    dayStart = (datetime.datetime.fromtimestamp(dayStart)).strftime('%H:%M')
    dayEnd   = (datetime.datetime.fromtimestamp(dayEnd)).strftime('%H:%M')

    return dayStart,dayEnd


# Removes all images taken during night time
def removeNight(dayStart, dayEnd, date):
    dirPath = "images/" + date

    # iterate through image directory
    for filename in os.listdir(dirPath):
        if filename.endswith(".jpg"):
            time = filename.strip('.jpg')
            
            # remove if night
            night = (time < dayStart) or (time > dayEnd)
            if night:
                path = dirPath + '/' + filename
                os.remove(path)
        

def main():
    yesterday = (datetime.datetime.today() - datetime.timedelta(1)).strftime('%Y-%m-%d')
    
    sunrise,sunset = sunriseAndSet(yesterday)
    
    dayStart,dayEnd = convertLocal(sunrise, sunset, TWILIGHT)
    
    removeNight(dayStart, dayEnd, yesterday) 


if __name__ == "__main__":
    main()
