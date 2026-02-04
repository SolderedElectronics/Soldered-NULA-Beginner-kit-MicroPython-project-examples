"""
@file		4.2_Auto_Scroll_Text.py
@brief		Example that uses 16x2 LCD Display and two pushbuttons to
            pause/resume the program execution demonstrating the use of
            hardware and timer based interrupts.

@author		Soldered
"""

# Import hardware classess for LCD communication, PIN configuration and Timer-based interrupts with external LCD driver
from machine import I2C, Pin, Timer
from LCD import LCD_I2C
import time

# Set up I2C connection with LCD display
i2c = I2C(0, scl=Pin(7), sda=Pin(6))
lcd = LCD_I2C(i2c)

# Configure button pins
BUTTON_A_PIN = 4
BUTTON_B_PIN = 5

# Initialize button objects on each pin, set to PULL-UP to set the pin in HIGH (1) state when not pressed
btn_A = Pin(BUTTON_A_PIN, Pin.IN, Pin.PULL_UP)
btn_B = Pin(BUTTON_B_PIN, Pin.IN, Pin.PULL_UP)

# Turn on the backlight of the LCD
lcd.backlight()
# Start communication with the LCD over I2C
lcd.begin()

# Print initial info
lcd.setCursor(0, 0)
lcd.print("Button A PAUSE")
lcd.setCursor(0, 1)
lcd.print("Button B RESUME")

# Pause for 2 seconds, clear the screen
time.sleep(2)
lcd.clear()

# Example sentance to display
sentence = "Autoscrolling example "

# Global flag to control program running state
paused = False
# Global flag to control timer interrupt
tick = False
# Debounce time
DEBOUNCE_MS = 30
# Last pressed time for buttons A and B
last_A = 0
last_B = 0

def irq_handler(pin):
    # Use global ('outside') variables to change the values outside the function
    global paused, last_A, last_B
    # Get current time in ms
    now = time.ticks_ms()
    # Check if button A was pressed
    if pin is btn_A:
        if time.ticks_diff(now, last_A) > DEBOUNCE_MS:
            # Update last pressed time for button A
            last_A = now
            # Update paused state
            paused = True
    # Button B pressed
    else:
        if time.ticks_diff(now, last_B) > DEBOUNCE_MS:
            # Update last pressed time for button B
            last_B = now
            # Update paused state
            paused = False

# Interrupt function triggered by timer every 0.4 seconds 
def on_tick(t):
    # Use global 'tick' variable
    global tick
    # Update tick state
    tick = True

# Attach interrupts to buttons A and B on pins 4 and 5
btn_A.irq(trigger=Pin.IRQ_FALLING, handler=irq_handler)
btn_B.irq(trigger=Pin.IRQ_FALLING, handler=irq_handler)

# Initialize timer interrupt to call 'on_tick' function every 0.4 seconds
tim = Timer(0)
tim.init(period=400, mode=Timer.PERIODIC, callback=on_tick)

# Enable autoscroll to the left direction
lcd.autoscroll()
# Set cursor to the last place in first row
lcd.setCursor(16, 0)

# Character index
i = 0
while True:
    # Check if scrolling is paused and if timer triggered
    if not paused:
        if tick:
            # Reset tick flag
            tick = False
            # Print next character
            lcd.print(sentence[i])
            # Move to the next character
            i += 1
            # Check if end of sentance has been reached
            if i >= len(sentence):
                # Reset index
                i = 0
                # Clear screen
                lcd.clear()
                lcd.setCursor(16, 0)
    # Small delay to avoid busy loop
    time.sleep_ms(10)
