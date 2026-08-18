"""
@file       7.5_Shift_Register.py
@brief      Project that shows how to drive many LEDs with only three pins of the board, using a 74HC595 shift
            register. The example builds a 4-bit binary counter that counts from 0 to 15 and displays the count on
            four LEDs, which is a nice way of seeing how computers count in binary.
            It introduces two new ideas: shifting data out one bit at a time, and latching the outputs.
            For details, connection diagram and more, check out the example documentation at: <link placeholder>

@author     Soldered
"""

from machine import Pin
import time

"""
This is a variable to which we pass the number of pin that we had connected the shift register's data pin to, marked DS
on the chip. This is the pin the bits themselves travel over, one after another.
The NULA board has a pin naming logic as follows: IO2, where 2 is the number that we give to the variable.
If you wish to use a different pin, make sure you are using a IO__ marked pin.

Remember that each of the four LEDs on the shift register outputs needs its own 330 Ohm resistor in series with it,
exactly as if it were wired straight to the board.
"""
DATA_PIN = 2

"""
This is a variable to which we pass the number of pin that we had connected the shift register's latch pin to. On the
74HC595 chip this pin is marked ST_CP. The latch is what tells the chip "the data I sent you is complete, show it now",
which is why the LEDs change all at once instead of flickering through every step.
"""
LATCH_PIN = 3

"""
This is a variable to which we pass the number of pin that we had connected the shift register's clock pin to, marked
SH_CP on the chip. The clock is a pin we switch up and down, and every time it goes up the chip takes in one more bit.
This is how the chip knows when the next bit is ready.
"""
CLOCK_PIN = 4

"""
Here we create our three Pin objects. Pin.OUT tells the board that these pins should write a value instead of reading
one, since all three of them send information to the chip.
"""
data_pin = Pin(DATA_PIN, Pin.OUT)
latch_pin = Pin(LATCH_PIN, Pin.OUT)
clock_pin = Pin(CLOCK_PIN, Pin.OUT)

# Start with all three pins low, so the chip begins from a known state.
data_pin.value(0)
latch_pin.value(0)
clock_pin.value(0)

"""
This variable holds the value of our counter. Each pass through the loop it grows by one, and after 15 it starts over
from zero.
"""
counter = 0


def shift_out(value):
    """
    This is a function we wrote ourselves, because MicroPython has no shiftOut() function the way Arduino does.
    It sends one byte out over the data pin, one bit at a time, pulsing the clock pin after each bit.
    range(7, -1, -1) counts down from 7 to 0, so we start with the most significant bit, meaning the leftmost one,
    which is the order the 74HC595 expects.
    Shifting the value right by i positions and combining it with 1 using the bitwise AND ("&") is how we pick out the
    single bit we want to send.
    """
    for i in range(7, -1, -1):
        bit = (value >> i) & 1
        data_pin.value(bit)
        clock_pin.value(1)
        clock_pin.value(0)


while True:

    """
    Here we keep our counter inside four bits. The "&" is a bitwise AND, and 0x0F is the hexadecimal way of writing the
    number 15, which in binary is 1111. Combining a number with 1111 this way keeps only its lowest four bits and throws
    the rest away, which is a common trick for making sure a value stays in range.
    """
    value = counter & 0x0F

    """
    Pulling the latch pin low tells the chip that we are about to send new data and that it should not change its
    outputs yet. Without this the LEDs would visibly flicker while the bits are still arriving.
    """
    latch_pin.value(0)

    # Send the eight bits of our value to the chip, using our own function above.
    shift_out(value)

    """
    Pulling the latch pin back high tells the chip that the data is complete. Only now do the outputs change, and all
    eight of them change together.
    """
    latch_pin.value(1)

    # Print the value too, so you can compare the number with the pattern of lit LEDs.
    print(value)

    """
    Count one up, and start over from zero once we pass 15, because four LEDs cannot show any number higher than that.
    The "%" operator gives the remainder of a division, which is a short way of wrapping a counter around.
    """
    counter = (counter + 1) % 16

    """
    time.sleep() is a function that starts a pause in the code, given in seconds. Half a second is slow enough to follow
    the counting with your eyes. Feel free to experiment with this value.
    """
    time.sleep(0.5)
