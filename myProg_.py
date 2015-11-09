#!/usr/bin/python
# Example using a character LCD plate.
import math
import time

import Adafruit_CharLCD as LCD

# Initialize the LCD using the pins 
lcd = LCD.Adafruit_CharLCDPlate()

keepGoing = True
curStatus = 0

#lcd.set_color(r,g,b)
def peakUse(curStatus):
	if (curStatus != 0):
		lcd.clear()
		lcd.set_color(1.0, 0.0, 0.0)
		lcd.message(time.asctime() + '\nPeak Usage')
	return 0

def partPeakUse(curStatus):
	if (curStatus != 1):
		lcd.clear()
		lcd.set_color(1.0, 1.0, 0.0)
		lcd.message(time.asctime() + '\nPart Peak Usage')
	return 1

def offPeakUse(curStatus):
	if (curStatus != 2):
		lcd.clear()
		lcd.set_color(0.0, 1.0, 0.0)
		lcd.message(time.asctime() + '\nOff Peak Usage')
	return 2

curStatus = peakUse(-1)
time.sleep(1)
curStatus = partPeakUse(curStatus)
time.sleep(1)
curStatus = offPeakUse(curStatus)
time.sleep(1)
lcd.clear()
lcd.set_color(0.0,0.0,1.0)
lcd.message('Starting...')
time.sleep(3)

curTime = time.localtime()
curStatus = -1
while keepGoing:
	if (curTime.tm_min != time.localtime().tm_min) :
		curStatus = -1
	curTime = time.localtime()
	#week day if less than 4
	if (curTime.tm_wday <= 4):
		#off-peak
		if (curTime.tm_hour < 7) :
			curStatus = offPeakUse(curStatus)
		#part-peak
		elif (curTime.tm_hour < 14) :
			curStatus = partPeakUse(curStatus)
		#peak
		elif (curTime.tm_hour < 21) :
			curStatus = peakUse(curStatus)
		#part-peak
		elif (curTime.tm_hour < 23) :
			curStatus = partPeakUse(curStatus)
		#off-peak
		else :
			curStatus = offPeakUse(curStatus)
	else :
		#off-peak
		if (curTime.tm_hour < 15) :
			curStatus = offPeakUse(curStatus)
		#peak
		elif (curTime.tm_hour < 19) :
			curStatus = peakUse(curStatus)
		#off-peak
		else :
			curStatus = offPeakUse(curStatus)

	if (lcd.is_pressed(LCD.SELECT)) :
		keepGoing = False

lcd.set_color(0.0,0.0,0.0)
lcd.clear()
lcd.message('Exited...')
