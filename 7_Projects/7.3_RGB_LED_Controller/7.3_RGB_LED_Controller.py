"""
@file     7.3_RGB_LED_Controller.py
@brief    Example that demonstrates how to control RGB LEDs using PWM based on
          the readings from a photoresistor (LDR).
          
@author   Soldered
"""

from machine import Pin, ADC, PWM
import time

# Pin configurations
LDR_PIN = 5       # Analog input pin for photoresistor
RED_PIN = 2       # PWM pin for red LED channel
GREEN_PIN = 3     # PWM pin for green LED channel
BLUE_PIN = 4      # PWM pin for blue LED channel
PWM_FREQ = 1000   # PWM frequency in Hz

# ADC setup for photoresistor
adc = ADC(Pin(LDR_PIN))

# PWM setup for RGB LEDs
pwm_r = PWM(Pin(RED_PIN), freq=PWM_FREQ)
pwm_g = PWM(Pin(GREEN_PIN), freq=PWM_FREQ)
pwm_b = PWM(Pin(BLUE_PIN), freq=PWM_FREQ)

# Function to map a value from one range to another
def map_range(x, in_min, in_max, out_min, out_max):
    if in_max == in_min:
        return out_min
    val = (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
    return max(min(val, max(out_min, out_max)), min(out_min, out_max))

# Main loop
while True:
    # Read LDR value
    ldr_value = adc.read() 
    print("LDR value:", ldr_value)

    # Map LDR value to RGB colors
    if ldr_value <= 1365:
        # Dark -> Red to Green
        r = map_range(ldr_value, 0, 1365, 255, 0)
        g = map_range(ldr_value, 0, 1365, 0, 255)
        b = 0
    elif ldr_value <= 2730:
        # Medium light -> Green to Blue
        r = 0
        g = map_range(ldr_value, 1366, 2730, 255, 0)
        b = map_range(ldr_value, 1366, 2730, 0, 255)
    else:
        # Bright -> Blue to White
        r = map_range(ldr_value, 2731, 4095, 0, 255)
        g = map_range(ldr_value, 2731, 4095, 0, 255)
        b = 255

    # Write PWM values to RGB pins
    pwm_r.duty(int(r * 1023 / 255))
    pwm_g.duty(int(g * 1023 / 255))
    pwm_b.duty(int(b * 1023 / 255))

    # Print RGB values
    print("RGB:", r, g, b)

    # Small delay
    time.sleep_ms(100)
