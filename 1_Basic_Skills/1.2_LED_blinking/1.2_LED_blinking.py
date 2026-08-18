"""
@file       1.2_LED_blinking.py
@brief      Example that shows how to control the blinking of a simple LED.
            For details, connection diagram and more, check out the example documentation at: <link placeholder>

@author     Soldered
"""

"""
Before we can use something, we have to import it. The machine module holds everything that talks to the hardware of
the board, and Pin is the part of it that controls a single pin. The time module lets us pause the program.
"""
from machine import Pin
import time

"""
This is a variable to which we pass the number of pin that we had connected the LED to.
The NULA board has a pin naming logic as follows: IO4, where 4 is the number that we give to the variable.
If you wish to use a different pin, make sure you are using a IO__ marked pin.

Remember that the LED needs a 330 Ohm resistor in series with it. That resistor limits how much current flows, and
without it the LED draws more than either it or the pin is built for, so both can be damaged.
"""
PIN_NUMBER = 4

"""
This is a variable that defines the blinking time, in seconds. Note that MicroPython counts in seconds here, while
Arduino counts in milliseconds, so 1 second and 1000 milliseconds mean the same thing.
Feel free to experiment with this value.
"""
DELAY_S = 1

"""
Here we create our Pin object, which we named "led". Creating it is what configures the pin: Pin.OUT tells the board
that this pin should write a value instead of reading one, the same job pinMode() does in Arduino.
This simply means that the pin "reads" the available data when in input mode, and "writes" data when in output mode.
As our pin needs to turn on the LED, we will put the pin in OUT mode.
"""
led = Pin(PIN_NUMBER, Pin.OUT)

"""
A while loop repeats the block below it for as long as its condition is true. Because True is always true, this loop
never ends, which is how MicroPython does what the loop() function does in Arduino.
"""
while True:

    """
    value() is a function that changes what our pin writes. As we are working with a digital pin, we can only switch
    between two values, high and low, written here as 1 and 0. Those values are represented by different voltage
    levels. On the NULA board, high is 3.3V while low is 0V. We will start with putting the pin high, giving the LED
    3.3V and lighting it up.
    """
    led.value(1)

    """
    time.sleep() is a function that starts a pause in the code. Its duration is given in seconds.
    In this case, we want to wait for a bit after we turned on the LED.
    """
    time.sleep(DELAY_S)

    # We put the pin low, turning the LED off.
    led.value(0)

    # Leave the LED turned off for a bit.
    time.sleep(DELAY_S)
