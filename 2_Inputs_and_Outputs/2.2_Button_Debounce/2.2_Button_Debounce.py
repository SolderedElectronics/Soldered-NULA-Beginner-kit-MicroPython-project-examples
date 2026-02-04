"""
@file		2.2_Button_Debounce.py
@brief		Example that shows how to implement button debounce logic to ensure
            only a single press is registered when a pushbutton is pressed.
            
@author		Soldered
"""

# Import necessary modules
from machine import Pin
import time

# Define pins used for LED and Pushbutton
led_pin = 5
button_pin = 19

# Create 'Pin' objects for LED and Pushbutton with LED set to output and button to input mode
led = Pin(led_pin, Pin.OUT)
btn = Pin(button_pin, Pin.IN, Pin.PULL_DOWN) # Turn on internal pull-down resistor so the pin reads as LOW (0) when the button is not pressed

# Set the initial LED state to low, keep track of last LED state (0 means not pressed in pull down configuration)
led.value(0)
last_state = 0

# Set debounce delay time in milliseconds
debounce_delay = 50

# Infinite loop
while True:
    # Read current voltage level of the button pin (0 when not pressed, 1 when pressed)
    current_state = btn.value()

    # Store the current time passed from the beginning of the program in milliseconds
    time_now = time.ticks_ms()

    # Check for moment when button state changes -> toggle the LED state accordingly
    if last_state == 0 and current_state == 1:
        if time.ticks_diff(time_now, time_now - debounce_delay) >= debounce_delay:
            print("Button pressed, toggling LED")
            led.toggle()  # Flips the LED state: ON -> OFF; OFF -> ON
    
    # Update last state
    last_state = current_state
    time.sleep_ms(10)  # Pause the program briefly to allow some time for CPU