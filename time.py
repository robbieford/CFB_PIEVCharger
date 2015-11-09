#!/usr/bin/python
# Example using a character LCD plate.
import math
import time

import Adafruit_CharLCD as LCD


# Initialize the LCD using the pins 
lcd = LCD.Adafruit_CharLCDPlate()

# Show some basic colors.

x = 0.0
y = 0.0
z = 0.0
keepGoing = True

while keepGoing:
	lcd.set_color(x, y, z)
	lcd.clear()
	lcd.message(time.asctime() + '\nr=' + str(x) + 'g=' + str(y) + 'b=' + str(z))
	time.sleep(5)
	x = x + 1.0
	if ( x > 1.05 ): 
		y = y + 1.0
		x = 0.0
	if ( y > 1.05 ):
		z = z + 1.0
		y = 0.0
	if ( z > 1.05 ):
		z = 0.0
	if (lcd.is_pressed(LCD.SELECT)) :
		keepGoing = False

lcd.set_color(0.0,0.0,0.0)
lcd.clear()
lcd.message('Exited...')
