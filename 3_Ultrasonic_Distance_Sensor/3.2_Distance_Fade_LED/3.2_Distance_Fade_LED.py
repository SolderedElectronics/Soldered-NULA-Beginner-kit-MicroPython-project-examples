"""
@file       3.2_Distance_Fade_LED.py
@brief      Example that shows how to control the brightness of an LED based on the distance measured by the
            Soldered Ultrasonic Distance Sensor. The closer an object is to the sensor, the brighter the LED
            becomes. This example introduces PWM and a map function, two tools that let us turn a measured value
            into a brightness level.
            For details, connection diagram and more, check out the example documentation at: <link placeholder>

@author     Soldered
"""

# The Soldered driver for the Ultrasonic Distance Sensor, found in the lib folder of this repository.
from UltrasonicSensor import UltrasonicSensor

"""
I2C is what the Qwiic connector carries, and the sensor is a Qwiic module.
PWM stands for Pulse Width Modulation. It switches a pin on and off very quickly, and the longer it stays on during
each cycle, the brighter an LED connected to it looks to our eyes. This is how MicroPython does what analogWrite()
does in Arduino.
"""
from machine import I2C, Pin, PWM
import time

"""
This is a variable to which we pass the number of pin that we had connected the LED to. Because we want to dim this
LED and not only switch it on and off, we drive it with PWM rather than with a plain Pin.
The NULA board has a pin naming logic as follows: IO2, where 2 is the number that we give to the variable.
If you wish to use a different pin, make sure you are using a IO__ marked pin.

Remember that the LED needs a 330 Ohm resistor in series with it. That resistor limits how much current flows, and
without it the LED draws more than either it or the pin is built for, so both can be damaged.
"""
LED_PIN = 2

"""
These two variables define the distance range we care about, in centimeters. Anything closer than the minimum counts
as "as close as possible" and anything further than the maximum counts as "far away". Feel free to experiment with
these values.
"""
MIN_DISTANCE = 2
MAX_DISTANCE = 50

"""
duty_u16() sets the brightness as a number from 0 (fully off) to 65535 (fully on), so 65535 is the largest brightness
we can ask for.
"""
MAX_BRIGHTNESS = 65535

"""
This is how long we wait after asking for a measurement, in milliseconds. The sensor gives up listening for an echo
after 38 milliseconds, so waiting a little longer than that means the answer is always ready when we ask for it.
"""
MEASURE_WAIT_MS = 50

"""
Here we set up the I2C connection. The two pins are fixed by the board: on the NULA MINI, I2C uses IO6 for the data
line (SDA) and IO7 for the clock line (SCL), which are exactly the pins the Qwiic connector is wired to.
"""
i2c = I2C(0, scl=Pin(7), sda=Pin(6))

"""
Here we create our sensor object, which we named "sensor", and hand it the I2C connection. We pass no pin numbers for
the sensor itself: every Qwiic module shares those same two I2C pins, and this sensor answers on address 0x30.
"""
sensor = UltrasonicSensor(i2c)

"""
Here we create our PWM object for the LED. freq() sets how fast the pin switches on and off. 5000 times per second is
far quicker than our eyes can follow, so we see a steady brightness instead of flickering.
"""
led = PWM(Pin(LED_PIN))
led.freq(5000)


def value_map(value, in_min, in_max, out_min, out_max):
    """
    This is a function we wrote ourselves, because MicroPython has no map() function the way Arduino does.
    It takes a number from one range and rescales it into another range. Handing it a distance between MIN_DISTANCE
    and MAX_DISTANCE gives us back a brightness, and because we will pass the output range reversed, the smallest
    distance produces the largest brightness.
    """
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


# begin() prepares the sensor for use, before we start reading from it.
sensor.begin()

# Print out the initial message so we know that the program started successfully.
print("Distance Fade LED Example started!")

while True:

    """
    Reading a Qwiic sensor takes two steps. takeMeasure() asks the sensor to send out a pulse and time the echo, and
    the wait afterwards gives it the moment it needs to finish that work and store the answer.
    """
    sensor.takeMeasure()
    time.sleep_ms(MEASURE_WAIT_MS)

    """
    getDistance() then fetches the stored answer, already converted into centimeters. The value comes back as a whole
    number of centimeters, which is all the accuracy this sensor can honestly offer.
    """
    distance = sensor.getDistance()

    """
    The sensor answers with 0 when it heard no echo at all, which happens when nothing is in range or when the surface
    in front of it scatters the sound away. That is not a real measurement, so we skip the rest of this pass instead of
    treating it as an object pressed right up against the sensor.
    continue jumps straight back to the top of the loop, ready for the next measurement.
    """
    if distance == 0:
        print("No echo received, nothing in range.")
        continue

    """
    Here we keep the measured distance inside the range we defined above. This is called clamping, and we do it because
    the next step expects a value inside a known range. Without it, an object 300 cm away would give us a brightness
    value far outside anything the LED can use.
    """
    if distance < MIN_DISTANCE:
        distance = MIN_DISTANCE
    if distance > MAX_DISTANCE:
        distance = MAX_DISTANCE

    """
    Here we turn the distance into a brightness with our own function above. Notice that the output range is
    reversed, from MAX_BRIGHTNESS down to 0: the smallest distance gives the largest brightness, which is exactly the
    effect we want.
    """
    brightness = value_map(distance, MIN_DISTANCE, MAX_DISTANCE, MAX_BRIGHTNESS, 0)

    # duty_u16() writes the brightness to the pin, and the LED changes at once.
    led.duty_u16(brightness)

    # Print both values, so we can see how the brightness changes together with the distance.
    print("Distance: {} cm -> Brightness: {}".format(distance, brightness))
