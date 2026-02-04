"""
@file		4.1_Print_Message.py
@brief		Example demonstrating how to use 16x2 LCD Display to display the time difference
            between button presses.

@author		Soldered
"""

# Import Pin and I2C to initialize communications with external LCD driver
from machine import I2C, Pin
from LCD import LCD_I2C
import time

# If you aren't using the Qwiic connector, manually enter your I2C pins
i2c = I2C(0, scl=Pin(7), sda=Pin(6))
lcd = LCD_I2C(i2c)

# Initialize sensor over Qwiic
# lcd = LCD_I2C()

# Initialize button on pin 5
BUTTON_PIN = 5
btn = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_DOWN) # Use internal PULL-DOWN to set the pin LOW (0) when the button is not pressed

# Function for printing new elapsed time each time button is pressed
def print_time_lcd(elapsed_time_s, isFirstPrint):
    # Check if button is pressed for first time, print accordingly
    if isFirstPrint:
        lcd.clear()
        lcd.setCursor(0, 0)
        lcd.print("Elapsed time: ")
    # Set cursor to point to first character in second row
    lcd.setCursor(0, 1)
    # Check if more than a minute has passed
    if elapsed_time_s < 60:
        # Print time in seconds format
        msg = "{:6.2f} s".format(elapsed_time_s)
    else:
        # Print time in MM:SS format
        minutes = int(elapsed_time_s / 60)
        seconds = int(elapsed_s % 60)
        msg = "{:02d}:{:02d} min".format(minutes, seconds)
    # Overwrite old text
    msg = (msg + " " * 16)[:16]
    # Print new text
    lcd.print(msg)

# Turn on the backlight of the LCD
lcd.backlight()

# Start communication with the LCD over I2C
lcd.begin()

# Hello world example
# Sets the cursor to the third character place in the first row
lcd.setCursor(2, 0)
lcd.print("Hello, World!")
# Sets the cursor to the first character place in the second row
lcd.setCursor(0, 1)
lcd.print("Press the button")

# Define timer variables for measuring elapsed time between button presses and debounce
last_press_MS = time.ticks_ms() 
DEBOUNCE_MS = 30 # Debounce time

# Flag to check if button was pressed for the first time or was already pressed
isFirstPrint = True

# Main loop to control the program
while True:
    # Get current button state
    current_state = btn.value()
    # Check if button was pressed
    if current_state == 1:
        # Check if enough time has passed since last press for debounce
        if time.ticks_diff(time.ticks_ms(), last_press_MS) >= DEBOUNCE_MS:
            if btn.value() == 0: # Additional debounce check to count only one press
                # Get elapsed time from last press in seconds
                elapsed_s = time.ticks_diff(time.ticks_ms(), last_press_MS) / 1000.0
                # Print elapsed time on LCD
                print_time_lcd(elapsed_s, isFirstPrint)
                # Update first print flag
                isFirstPrint = False
            
                # Reset timer
                last_press_MS = time.ticks_ms()
                
                # Wait until button is released to avoid repeated triggers
                while btn.value() == 0:
                    time.sleep_ms(10)
