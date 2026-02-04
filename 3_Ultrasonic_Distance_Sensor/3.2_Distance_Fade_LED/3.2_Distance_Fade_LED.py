"""
@file		3.2_Distance_Fade_LED.py
@brief		An example demonstrating how to use an ultrasonic sensor to control
            the brightness of an LED.

@author		Soldered
"""

# Import necessary modules
from UltrasonicSensor import UltrasonicSensor
from machine import Pin, PWM
import time

# Create I2C and 'UltrasonicSensor' object which initializes the sensor in Qwiic mode with default I2C pins
#i2c = I2C(0, scl=Pin(7), sda=Pin(6))
sensor = UltrasonicSensor(trig_pin=4, echo_pin=3)

# Create 'Pin' object on GPIO 5, use it to create a 'PWM' object on that pin with frequency set to 5000 Hz
led = Pin(5)
led_pwm = PWM(led)
led_pwm.freq(5000)

# Define 'map' function to map a value from one range to another
# We use it to map distance (cm) to 10-bit PWM duty for LED brightness
# Arguments: input value, min and max input values from sensor, min and max output values
def map_distance_value(value, in_min, in_max, out_min, out_max):
    if value < in_min:
        value = in_min
    elif value > in_max:
        value = in_max
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Infinite loop to conitunuosly read sensor values and control the LED
while True:
    #sensor.takeMeasure()
    # Add small delay for measurement
    time.sleep(0.1)
    # Store sensor reading in distance variable (value in cm)
    distance = sensor.getDistance()
    print(distance)
    # Set distance to 400 cm for very far objects
    if distance > 400:
        distance = 400
    # Map distance value (0 - 400) to PWM duty cycle (1023 - 0) and store it in pwm_value variable
    # Shorter distance -> brighter LED; Longer distance -> Lower brightness
    pwm_value = map_distance_value(distance, 0, 400, 1023, 0)
    # Set LED PWM duty
    led_pwm.duty(pwm_value)
    # Pause the program so the echoes from last ping 'die out'
    time.sleep(0.25)
