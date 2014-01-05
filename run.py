#!/usr/bin/env python

import gaugette.rotary_encoder
import gaugette.switch
import gaugette.rgbled
import wiringpi2
import picamera
import time
from datetime import datetime
import os
import glob
import shutil
import subprocess
import pytumblr
client = pytumblr.TumblrRestClient(
    'My8z0HtATDPFiQYPHtEXELMdZJgryHvJpiDVrC61lEEhiy0Sbm',
    'EaHnvYX9NB4rfRONWFHw4BIJjAAyfwF4zXLoMReG5IR7lmYr4D',
    'cCgzb9qfYwBiBC3l2nEm9Zq91t0mdY3UIKsvZXEBboDQqpSVFa',
    'o6M3ZLBw6Ud7aTFjEGWwr90i8CQOpEfAwZeknnaMdP5h8akaI0',
)

recPath = '/home/pi/crank/stills/'
io = wiringpi2.GPIO(wiringpi2.GPIO.WPI_MODE_PINS)

led = gaugette.rgbled.RgbLed(11,13,15)
A_PIN  = 7
B_PIN  = 9
encoder = gaugette.rotary_encoder.RotaryEncoder.Worker(A_PIN, B_PIN)
encoder.start()
last_state = None
rotCount = 0
antiRotCount = 0
gifPath = '/home/pi/crank/gifs/'
cam = picamera.PiCamera()
cam.resolution = (320,240)
while True:
	delta = encoder.get_delta()
	if delta < 0:
		print delta
		antiRotCount = 0
		rotCount = rotCount + 1
		cam.capture(recPath + str(rotCount) +'.jpg', use_video_port=True)
	if delta > 0:
		print antiRotCount
		antiRotCount = antiRotCount + 1
		if antiRotCount == 60:

			print 'done capturing frames'
			recTime =   time.strftime("%Y%m%d-%Hh%Mm-%Ss")
			print 'converting'
			subprocess.call('mplayer mf://'+recPath+'*.jpg -mf w=320:h=240:type=jpg -vf scale=320:240 -vo gif89a:fps=5:output='+ gifPath + recTime+'.gif', shell=True)
			print 'chmodding'
			subprocess.call('chmod 777 ' + gifPath + recTime + '.gif', shell=True)
			print 'tumbling...'
			client.create_photo('crankcrankgif.tumblr.com', data= gifPath + recTime + '.gif')
			dst_dir = recPath + recTime
			print 'make dir'
			os.makedirs(dst_dir)
			print 'move files'
			for jpgfile in glob.iglob(os.path.join(recPath, "*.jpg")):
				shutil.move(jpgfile, dst_dir)
			antiRotCount = 0
		#print rotCount
    #sw_state = switch.get_state()
    #if sw_state != last_state:
    #    print "switch %d" % sw_state
     #   last_state = sw_state
