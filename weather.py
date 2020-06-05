#!/usr/bin/env python3

# This script pulls the current weather data from the OpenWeather api

import json
import requests
import datetime
import os

# API Variables
cityName    = "Winnipeg"
countryCode = "ca"
apiKey      = "4dac3c68a1b48a72f20ed2a775531b0d"
baseUrl     = "http://api.openweathermap.org/data/2.5/weather?"

# Gets the directory to store weather data or creates one if it does not already exist
now = datetime.datetime.now()
dir = "weather/%s" % now.strftime("%Y-%m-%d")
if not os.path.exists(dir):
    os.makedirs(dir)

# Gets weather data from OpenWeather
completeUrl = baseUrl + "q=" + cityName + "," + countryCode + "&appid=" + apiKey
response = requests.get(completeUrl)

# Convert to JSON and store
r = response.json()
with open('%s/%s.json' % (dir, now.strftime("%H:%M")), 'w') as file:
    json.dump(r, file)
