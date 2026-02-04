"""
@file		7.5_Shift_Register.py
@brief		Uses a 74HC595 shift register to create a 4-bit binary counter, counting 
            from 0 to 15, with each number displayed in binary using 4 LEDs.

@author		Soldered
"""

from machine import Pin
import time

# --- Pin setup ---
latchPin = Pin(5, Pin.OUT)  # ST_CP (Latch)
clockPin = Pin(19, Pin.OUT)  # SH_CP (Clock)
dataPin  = Pin(18, Pin.OUT)  # DS (Data)

# Initialize pins
latchPin.value(0)
clockPin.value(0)
dataPin.value(0)

counter = 0  # 4-bit counter

# --- Function to shift out a byte MSB-first ---
def shift_out(data_pin, clock_pin, value):
    for i in range(7, -1, -1):  # MSB first
        bit = (value >> i) & 1
        data_pin.value(bit)
        clock_pin.value(1)
        clock_pin.value(0)

# --- Main loop ---
while True:
    value = counter & 0x0F  # Keep only lower 4 bits

    latchPin.value(0)            # Prepare shift register
    print(value)              # Debug: print current value
    shift_out(dataPin, clockPin, value)
    latchPin.value(1)            # Latch outputs to LEDs

    counter = (counter + 1) % 16

    time.sleep(1)              # 1 second delay
    