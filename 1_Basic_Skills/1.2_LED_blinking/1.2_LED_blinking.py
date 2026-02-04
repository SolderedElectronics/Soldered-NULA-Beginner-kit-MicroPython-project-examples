"""
@file		1.2_LED_blinking.py
@brief		Example that shows how to blink a simple LED.

@author		Soldered
"""

# To control the LED connected to microcontroller, we import Pin from the built-in 'machine' module,
# to create delays, we import 'time' which allows us to pause the program execution
from machine import Pin
import time

# We are storing the pin number which we connect the LED with
pin_number = 5

# Here we create a Pin object named 'led' that is used to control the actual pin on the board,
# we pass in the pin number and specifiy the pin to be an output to send signals to it 
led = Pin(pin_number, Pin.OUT)

# This sets the pins voltage to low (turn off LED)
led.value(0)

# Start infinite loop which runs forever until we stop the program,
# alternating between 'high' state and 'low' state
while True:
    led.value(1)		# Turn LED on
    time.sleep(1)		# Pause for 1 sec
    led.value(0)		# Turn LED off
    time.sleep(1)		# Pause for 1 sec

