"""
@file       3.1_Measuring_Distance.py
@brief      Example that shows how to measure distance using the Soldered Ultrasonic Distance Sensor.
            The sensor sends out a short ultrasonic pulse and then listens for its echo. It measures how long the
            echo took to come back, works out the distance from that time, and hands us the answer over Qwiic.
            The measured distance is printed in centimeters to the console.
            For details, connection diagram and more, check out the example documentation at: <link placeholder>

@author     Soldered
"""

"""
I2C is a way for several devices to talk to the board over just two wires, and it is what the Qwiic connector carries.
We need it here because the sensor is a Qwiic module.
"""
from machine import I2C, Pin

"""
Importing a module gives us access to ready-made functions that do the hard work for us. Here we import the Soldered
driver for the Ultrasonic Distance Sensor, so we don't have to time the echo ourselves.
This driver lives in the lib folder of this repository. Copy the whole lib folder onto your board, otherwise
MicroPython will not be able to find it.
"""
from UltrasonicSensor import UltrasonicSensor
import time

"""
Here we set up the I2C connection. The two pins are fixed by the board: on the NULA MINI, I2C uses IO6 for the data
line (SDA) and IO7 for the clock line (SCL), which are exactly the pins the Qwiic connector is wired to.
Unlike Arduino, MicroPython does not find these on its own, so we always name them.
"""
i2c = I2C(0, scl=Pin(7), sda=Pin(6))

"""
Here we create our sensor object, which we named "sensor", and hand it the I2C connection. An object is our way of
talking to the sensor: every function we call on it, we call through this name.
Notice that we pass no pin numbers for the sensor itself. Every Qwiic module shares the same two I2C pins, which is why
you can chain several of them together, and this sensor answers on address 0x30.
"""
sensor = UltrasonicSensor(i2c)

"""
This is how long we wait after asking for a measurement, in milliseconds. The sensor needs a moment to send its pulse
out and listen for the echo, and it gives up after 38 milliseconds if no echo comes back. We wait a little longer than
that so the answer is always ready by the time we ask for it.
"""
MEASURE_WAIT_MS = 50

"""
begin() prepares the sensor for use. A sensor should always be initialized before we start reading from it.
"""
sensor.begin()

# Print out the initial message so we know that the program started successfully.
print("Ultrasonic Measuring Distance Example started!")
print("Move an object in front of the sensor to see the distance change.")

# A while True loop repeats forever, which is how MicroPython does what the loop() function does in Arduino.
while True:

    """
    Reading a Qwiic sensor takes two steps. takeMeasure() is the first one: it asks the sensor to send out a pulse and
    time the echo. The sensor does that work on its own and remembers the answer, which is why we then have to wait
    before collecting it.
    """
    sensor.takeMeasure()
    time.sleep_ms(MEASURE_WAIT_MS)

    """
    getDistance() is the second step: it fetches the answer the sensor worked out and stored, already converted into
    centimeters. The value comes back as a whole number of centimeters, which is all the accuracy this sensor can
    honestly offer.
    """
    distance = sensor.getDistance()

    """
    The sensor answers with 0 when it heard no echo at all, which happens when nothing is in range or when the surface
    in front of it scatters the sound away. That is not a real measurement, so we say so rather than reporting a
    distance of zero centimeters, which would suggest an object touching the sensor.
    """
    if distance == 0:
        print("No echo received, nothing in range.")
    else:
        print("Distance: {} cm".format(distance))

    """
    time.sleep() is a function that starts a pause in the code, given in seconds. Without this pause the readings
    would scroll by far too quickly to read, and it also lets the echoes of the last pulse die out before we ask for
    the next one. Feel free to experiment with this value.
    """
    time.sleep(0.5)
