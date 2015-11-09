#!/usr/bin/python
# Example using a character LCD plate.
import math
import time
import datetime
import subprocess

import Adafruit_CharLCD as LCD

# Initialize the LCD using the pins 
lcd = LCD.Adafruit_CharLCDPlate()

lcd.create_char(1, [1, 1, 1,  5, 9, 31, 8, 4])
lcd.create_char(2, [2, 4, 8, 31, 8, 4, 2, 0])
lcd.create_char(3, [4, 14, 21, 4, 4, 4, 4, 4])
lcd.create_char(4, [4, 4, 4, 4, 4, 21, 14, 4])
lcd.create_char(5, [8, 4, 2, 31, 2, 4, 8, 0])

#lcd.set_color(r,g,b)
def peakUse(curStatus):
	if (curStatus != 0):
		lcd.clear()
		lcd.set_color(1.0, 0.0, 0.0)
		lcd.message(time.strftime('%H:%M') + ' - Peak')
		lcd.message('\nMenu \x01\x02\x03\x04\x05')
	return 0

def partPeakUse(curStatus):
	if (curStatus != 1):
		lcd.clear()
		lcd.set_color(1.0, 1.0, 0.0)
		lcd.message(time.strftime('%H:%M') + ' - Partial')
		lcd.message('\nMenu \x01\x02\x03\x04\x05')
	return 1

def offPeakUse(curStatus):
	if (curStatus != 2):
		lcd.clear()
		lcd.set_color(0.0, 1.0, 0.0)
		lcd.message(time.strftime('%H:%M') + ' - Off Peak')
		lcd.message('\nMenu \x01\x02\x03\x04\x05')
	return 2

def menu():
	lcd.set_color(1.0, 1.0,1.0)
	lastState = -1
	menuState = 0
	while True:
		if (menuState == 0 and lastState != 0):
			lcd.clear()
			lcd.message('Charge Now \x01\n\x02 Back       \x03\x04')
			menuState = 0
		if (menuState == 1 and lastState != 1):
			lcd.clear()
			lcd.message('Delay Charge \x01\n\x02 Back       \x03\x04')
			menuState = 1
		if (menuState == 2 and lastState != 2):
			lcd.clear()
			lcd.message('Restart System \x01\n\x02 Back       \x03\x04')
			menuState = 2
		if (menuState == 3 and lastState != 3):
			lcd.clear()
			lcd.message('Exit \x01\n\x02 Back       \x03\x04')
			menuState = 3

		if (lcd.is_pressed(LCD.SELECT) or lcd.is_pressed(LCD.RIGHT)):
			if (menuState == 0):
				Override()
				return True
			elif (menuState == 1):
				DelayCharge()
				return True
			elif (menuState == 2):
				lcd.clear()
				lcd.message('Restarting...')
				subprocess.call(['sudo reboot'], shell=True)
				return False
			else :
				lcd.set_color(0.0,0.0,0.0)
				lcd.clear()
				lcd.message('Exited...')
				return False
		if (lcd.is_pressed(LCD.LEFT)):
			return True

		if (lcd.is_pressed(LCD.UP)):
			menuState-=1
			if (menuState < 0) :
				menuState = 3
		elif (lcd.is_pressed(LCD.DOWN)):
			menuState+=1
			if (menuState > 3) :
				menuState = 0
		else:
			lastState = menuState
			
def DelayCharge():
	lcd.clear()
	lcd.message('Do something...')

def Override() :
	settingTime = True
	overrideMins = 0
	lastMins = -1
	while (settingTime) :
		if (overrideMins != lastMins):
			lcd.clear()
			lcd.message('Time:    ' + str(overrideMins) + 'mins')
			lcd.message('\n\x02 Exit   \x03\x04    \x01')
			lastMins = overrideMins
		if (lcd.is_pressed(LCD.DOWN)) :
			if (overrideMins >=15) :
				overrideMins-=15
		if (lcd.is_pressed(LCD.UP)):
			if (overrideMins <= 225):
				overrideMins+=15
		if (lcd.is_pressed(LCD.LEFT)):
			return
		if (lcd.is_pressed(LCD.SELECT) or lcd.is_pressed(LCD.RIGHT)) :
			settingTime = False
	
	lcd.clear()
	lcd.message('Charger active\nfor ' + str(overrideMins) + ' mins')
	time.sleep(5)
	countingDown = True
	lastMin = -1
	while (countingDown) :
		if (lastMin != time.localtime().tm_min):
			lastMin = time.localtime().tm_min
			lcd.clear()
			lcd.message(str(overrideMins) + ' mins left\n')
			lcd.message('\x02 Exit')
			overrideMins-=1
		if (overrideMins < 0 or lcd.is_pressed(LCD.LEFT)):
			countingDown = False
			

curStatus = peakUse(-1)
time.sleep(0.5)
curStatus = partPeakUse(curStatus)
time.sleep(0.5)
curStatus = offPeakUse(curStatus)
time.sleep(0.5)
lcd.clear()
lcd.set_color(0.0,0.0,1.0)
lcd.message('Starting...')
time.sleep(2)

def running() :
	curTime = time.localtime()
	curStatus = -1
	keepGoing = True
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

		if (lcd.is_pressed(LCD.SELECT) or lcd.is_pressed(LCD.LEFT) or
			lcd.is_pressed(LCD.RIGHT) or lcd.is_pressed(LCD.UP) or
			 lcd.is_pressed(LCD.DOWN)) :
			curStatus = -1
			keepGoing = menu()

running()

