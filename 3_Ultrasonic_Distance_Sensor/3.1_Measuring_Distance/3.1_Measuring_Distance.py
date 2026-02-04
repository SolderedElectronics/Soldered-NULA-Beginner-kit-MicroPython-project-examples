"""
@file        3.1_Measuring_Distance.py
@brief       Example that demonstrates how to measure distance using an ultrasonic
             distance sensor (HC-SR04).

@author      Soldered
"""

# To get distance readings from HC-SR04 ultrasonic sensor we import the UltrasonicSensor module
# This UltrasonicSensor class supports both 'native (GPIO)' and 'Qwiic (I2C)' modes
from UltrasonicSensor import UltrasonicSensor
import time

# Create I2C and 'UltrasonicSensor' object which initializes the sensor in Qwiic mode with default I2C pins
#i2c = I2C(0, scl=Pin(7), sda=Pin(6))
sensor = UltrasonicSensor(trig_pin=4, echo_pin=3)

# Infinite loop to continuously read sensor values
while True:
    # Add small delay for measurement
    time.sleep(0.1)  

    # Sensor sends out a pulse and waits for the echo to return, we then use the time
    # it took for the echo to return to calculate the distance in centimeters to the object
    distance = sensor.getDistance()  

    # Small delay for measurement
    time.sleep(0.1)

    # Store sensor reading in duration variable (value in microseconds)
    duration = sensor.getDuration()  

    print(f"Distance: {distance} cm")  # Print the distance value to the console
    print(f"Duration: {duration} us")  # Print the duration value to the console

    # Pause the program so the echoes from last ping 'die out'
    time.sleep(0.25)  
