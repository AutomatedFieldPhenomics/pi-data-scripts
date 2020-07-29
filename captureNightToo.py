#!/usr/bin/env python3
from picamera import PiCamera
from time import sleep
import datetime
import os
from gpiozero import LED
camera = PiCamera()
camera.start_preview()
#camera.rotation = 90
led1 = LED(23)
led2 = LED(24)
led1.on()
led2.on()
sleep(2)
now = datetime.datetime.now()
dir = "images/%s" % now.strftime("%Y-%m-%d")
if not os.path.exists(dir):
	os.makedirs(dir)
camera.capture('%s/%s.png' % (dir, now.strftime("%H:%M:%S")))
camera.stop_preview()
led1.off()
led2.off()
