"""
@file		7.8_Parking_Sensor_Project.py
@brief		Example demonstrating how to use an ultrasonic sensor with a buzzer
            to generate sound based on the measured distance. The buzzer's beeping frequency
            changes as objects get closer, simulating a car parking sensor system.

@author		Soldered
"""

# To control the buzzer import Pin and PWM classes, import UltrasonicSensor module for sensor readings
# Import time to control periods for buzzer play time
from UltrasonicSensor import UltrasonicSensor
from machine import I2C, Pin, PWM
import time

# Constants to control sound behavior
CONTINUOUS_THRESHOLD_CM = 35 # Below this threshold - play continous tone
BEEP_START_DIST_CM = 170 # No sound if measured distance is beyond this value
MIN_BEEP_PERIOD_MS = 60 # Shortest beep cycle (fastest beeping rate)
MAX_BEEP_PERIOD_MS = 700 # Longest beep cycle (slowest beeping rate)
MAX_BEEP_ON_TIME_MS = 50 # Max play time for each 'beep'

# Buzzer pin value and PWM settings
BUZZ_PIN = 5
BUZZ_FREQ_HZ = 2000
BUZZ_DUTY = 30000

# Configure PWM pin with defined settings to control the buzzer
buzz_pwm = PWM(Pin(BUZZ_PIN))
buzz_pwm.freq(BUZZ_FREQ_HZ)
buzz_pwm.duty_u16(0)

#i2c = I2C(0, scl=Pin(7), sda=Pin(6))

# Initialize Ultrasonic sensor object
sensor = UltrasonicSensor(trig_pin=19, echo_pin=18)

# Timing variables - time.ticks_ms() returns the number of milliseconds since the board was powered on
MEAS_PERIOD_MS = 80 # Value that sets how often to take distance measurements
last_meas = time.ticks_ms() # Store timestamp of last distance measurement
last_toggle = time.ticks_ms() # Track timestamp of last time buzzer changed state
beep_on = False # Flag to save buzzer state
period_ms = -1 # Sound behavior : -1 = silent, 0 = continuous, > 0 = beep period
BEEP_ON_TIME_MS = 0 # Duration of play time (ON time) of each beep

# Map function used to map distance to beep period
def map_distance_value(value, in_min, in_max, out_min, out_max):
    if value < in_min:
        value = in_min
    elif value > in_max:
        value = in_max
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Main loop
while True:
    # Store current 'clock' time
    now = time.ticks_ms()
    
    # ticks_diff() used for measuring difference between 2 tick values
    # If 80 ms passed -> get reading & play sound
    if time.ticks_diff(now, last_meas) >= MEAS_PERIOD_MS:
        sensor.takeMeasure()
        last_meas = now # Store the time of measurement
        distance = sensor.getDistance() # Get distance from sensor
        # Choose 'sound mode' based on measured distance
        if distance <= CONTINUOUS_THRESHOLD_CM:
            period_ms = 0 # Set to continuous
        elif distance >= BEEP_START_DIST_CM:
            period_ms = -1 # Set to silent
        else:
            # Map distance reading from [35, 200] to a beep period [60, 700], store in period_ms
            period_ms = map_distance_value(distance, CONTINUOUS_THRESHOLD_CM, BEEP_START_DIST_CM, MIN_BEEP_PERIOD_MS, MAX_BEEP_PERIOD_MS)
        # Define duration of the 'ON time' of each beep, make the beep last a quarter of period cycle,
        # always between 10 and 50 milliseconds
        on_time = int(period_ms / 4)
        if on_time < 10:
            on_time = 10
        elif on_time > MAX_BEEP_ON_TIME_MS:
            on_time = MAX_BEEP_ON_TIME_MS
        BEEP_ON_TIME_MS = on_time

    # Based on period_ms, turn the buzzer ON or OFF depending on mode    
    # Continuous mode 
    if period_ms == 0:
        if not beep_on: # If the buzzer isn't ON
            # Play continuous sound and keep it turned ON
            buzz_pwm.duty_u16(BUZZ_DUTY)
            beep_on = True
            
    # Silent mode
    elif period_ms == -1:
        if beep_on: # If the buzzer is ON
            # Turn off buzzer
            buzz_pwm.duty_u16(0)
            beep_on = False
            
    # Beeping mode
    else:
        if not beep_on: # Currently OFF
            # Wait for 'silent' part to finish (period_ms - BEEP_ON_TIME_MS), then turn it ON
            if time.ticks_diff(now, last_toggle) >= (period_ms - BEEP_ON_TIME_MS):
                buzz_pwm.duty_u16(BUZZ_DUTY) # Turn ON buzzer
                beep_on = True # Change state
                last_toggle = now # Track toggle time
        else: # Currently ON
            # Wait until 'ON-time (BEEP_ON_TIME_MS)' has passed, then turn if OFF
            if time.ticks_diff(now, last_toggle) >= BEEP_ON_TIME_MS:
                buzz_pwm.duty_u16(0) # Turn OFF buzzer
                beep_on = False # Change state
                last_toggle = now # Track toggle time
