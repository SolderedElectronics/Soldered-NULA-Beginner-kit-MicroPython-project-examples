"""
@file		2.1_Button_Counter.py
@brief		Example that shows the use of pushbutton to count how many
            times a button was pressed.

@author		Soldered
"""

# Import necessary modules
from machine import Pin
import time

# Define pin used for pshbutton
button_pin = 19

# Create 'Pin' objects for LED and Pushbutton with LED set to output and button to input mode
btn = Pin(button_pin, Pin.IN, Pin.PULL_DOWN) # Turn on internal pull-down resistor so the pin reads as LOW (0) when the button is not pressed

# Initialize counter variable to keep track of button presses
counter = 0

while True:
    # Read current voltage level of the button pin (0 when not pressed, 1 when pressed)
    current_state = btn.value()

    # Check for moment when button is pressed, pull-down configuration reads LOW (0) when not pressed
    # and HIGH (1) when pressed
    if current_state == 1:
        # Increment counter variable and print its value to the console
        counter += 1
        print("Button pressed, count:", counter)

    time.sleep_ms(10) # Pause the program briefly to allow some time for CPU
