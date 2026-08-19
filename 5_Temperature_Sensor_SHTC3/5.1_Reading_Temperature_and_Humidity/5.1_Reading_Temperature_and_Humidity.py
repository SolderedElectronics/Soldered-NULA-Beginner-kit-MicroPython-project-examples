"""
@file       5.1_Reading_Temperature_and_Humidity.py
@brief      Example that shows how to measure temperature and humidity using the Soldered SHTC3 sensor.
            The sensor communicates over Qwiic, so only one cable is needed. The measured values are printed
            to the console.
            For details, connection diagram and more, check out the example documentation at: <link placeholder>

@author     Soldered Electronics
"""

# I2C is what the Qwiic connector carries, and the SHTC3 is a Qwiic module.
from machine import I2C, Pin

# The Soldered driver for the SHTC3 sensor, found in the lib folder of this repository.
from SHTC3 import SHTC3
import time

"""
Here we set up the I2C connection. On the NULA MINI, I2C uses IO6 for the data line (SDA) and IO7 for the clock line
(SCL), which are exactly the pins the Qwiic connector is wired to. Notice that we never define a pin for the sensor
itself: every Qwiic module shares these same two pins, which is why you can chain several of them together.
"""
i2c = I2C(0, scl=Pin(7), sda=Pin(6))

"""
Here we create our sensor object, which we named "shtc_sensor", and hand it the I2C connection. An object is our way
of talking to the sensor: every function we call on it, we call through this name.
"""
shtc_sensor = SHTC3(i2c)

"""
This variable defines how much time passes between two measurements, in milliseconds. 2000 milliseconds is two
seconds. Feel free to experiment with this value.
"""
UPDATE_MS = 2000

"""
This variable remembers the moment when we took the last measurement. We compare it against the current time to know
when the next measurement is due.
"""
last_update = 0

"""
begin() prepares the sensor for use and starts the communication. It also tells us whether the sensor answered: the
function gives back True on success and False on failure. We check the result and print a message either way, so that
if nothing shows up later we know whether the problem is the cable or the code.
The "not" in front means the opposite, so this reads as "if the sensor did not start".
"""
if not shtc_sensor.begin():
    print("SHTC3 initialization failed!")
else:
    print("SHTC3 sensor ready!")

while True:

    """
    time.ticks_ms() is a function that returns the number of milliseconds passed since the board was powered on. We
    use it instead of a plain sleep so that the board stays free to do other work between measurements, which matters
    as soon as your program has more than one job.
    This counter eventually wraps around back to zero, which is why we always use time.ticks_diff() to work out the
    difference between two of these numbers instead of subtracting them ourselves.
    """
    now = time.ticks_ms()

    """
    Here we check how much time has passed since the last measurement. Only when UPDATE_MS milliseconds have gone by
    do we take a new reading, and we immediately remember the current time as the new starting point.
    """
    if time.ticks_diff(now, last_update) >= UPDATE_MS:
        last_update = now

        """
        sample() tells the sensor to perform a fresh measurement and store the result inside itself. We have to call
        it before reading the values, otherwise we would keep getting the result of the previous measurement.
        """
        shtc_sensor.sample()

        """
        readTemperature() returns the temperature from the last measurement in degrees Celsius, and readHumidity()
        returns the relative humidity in percent. Both are decimal numbers.
        """
        temperature = shtc_sensor.readTemperature()
        humidity = shtc_sensor.readHumidity()

        """
        Here we build one readable line out of both values. The curly braces are filled in with our values, and
        ":.2f" tells Python to show a number with two decimal places.
        """
        print("Temperature: {:.2f} °C, Humidity: {:.2f} %".format(temperature, humidity))

    # A very short pause leaves the processor a moment to handle its own background work.
    time.sleep_ms(10)
