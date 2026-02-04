"""
@file		7.2_LED_Traffic_Light.py
@brief		Example project utilizing LEDs to simulate a traffic light system.
            The LEDs change colors in a sequence to represent traffic light signals.

@author		Soldered
"""

# Import necessary modules
from machine import Pin, Timer
import time

# Define LED pins
RED_LED_PIN = 5
YELLOW_LED_PIN = 4
GREEN_LED_PIN = 3

request_red = False
green_light_on = False
button_timeout_expired = True
last_button_press = 0

# Timer to handle button timeout
timeout_timer = Timer(0)

def irq_handler(pin):
    if green_light_on and button_timeout_expired:
        global request_red, last_button_press
        # Debounce catwalk button
        if time.ticks_diff(time.ticks_ms(), last_button_press) >= 500:
            last_button_press = time.ticks_ms()
            print("Catwalk button pressed!")
            request_red = True

def blink_green():
    for _ in range(4):
        green_led.value(0)
        time.sleep(0.5)
        green_led.value(1)
        time.sleep(0.5)

def green_off_sequence():
    global green_light_on
    green_light_on = False
    blink_green()
    green_led.value(0)
    yellow_led.value(1)
    time.sleep(3)
    yellow_led.value(0)

def timeout_handler(t):
    global button_timeout_expired
    button_timeout_expired = True
    print("Button timeout expired, can request red light again.")

# Define pushbutton pin
BUTTON_PIN = 18
# Define button pin and attach interrupt handler
catwalk_button = Pin(18, Pin.IN, Pin.PULL_UP)
catwalk_button.irq(trigger=Pin.IRQ_FALLING, handler=irq_handler)

# Initialize LED pins as outputs
red_led = Pin(RED_LED_PIN, Pin.OUT)
yellow_led = Pin(YELLOW_LED_PIN, Pin.OUT)
green_led = Pin(GREEN_LED_PIN, Pin.OUT)

# Turn off all LEDs initially
red_led.value(0)    
yellow_led.value(0)
green_led.value(0)

# Initialize pushbutton pin
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

while True:
    red_led.value(1)    # Turn on red LED
    time.sleep(5)      # Wait for 10 seconds

    yellow_led.value(1) # Turn on yellow LED
    time.sleep(3)       # Wait for 3 seconds

    red_led.value(0)    # Turn off red LED
    yellow_led.value(0) # Turn off yellow LED
    green_led.value(1)  # Turn on green LED

    green_light_start = time.ticks_ms()
    while True:
        green_light_on = True
        # If 10 seconds passed, end green light
        if time.ticks_diff(time.ticks_ms(), green_light_start) > 10000:
            green_off_sequence()
            break
        if button_timeout_expired:
            if request_red == True:
                green_off_sequence()
                request_red = False
                button_timeout_expired = False
                timeout_timer.init(period=25000, mode=Timer.ONE_SHOT, callback=timeout_handler)
                break

