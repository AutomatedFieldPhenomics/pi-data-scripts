#!/usr/bin/env python3

# This script captures images using picamera, additional code has been added to prevent taking images when the light levels are below a certain point

from picamera import PiCamera
from time import sleep
import datetime
import os
import ts12591

LUX_THRESHOLD = 1

def capture():
    camera = PiCamera()
    camera.resolution = (720, 480)
    camera.rotation = 180

    # start preview seems to be necessary for white balance and auto exposure
    camera.start_preview()
    sleep(2)

    now = datetime.datetime.now()

    dir = "images/%s" % now.strftime("%Y-%m-%d")
    if not os.path.exists(dir):
        os.makedirs(dir)

    camera.capture('%s/%s.png' % (dir, now.strftime("%H:%M:%S")))

    camera.stop_preview()
    return

def getLux():
    tsl = tsl2591.Tsl2591()
    full, ir = tsl.get_full_luminosity()
    lux = tsl.calculate_lux(full, ir)
    return lux

def main():
    lux = getLux()

    if lux > LUX_THRESHHOLD:
        capture()

if __name__ == "__main__":
    main()
