"""
@file       2.3_Photoresistor_Analog_Read.py
@brief      Example that shows how to read light intensity using a photoresistor (LDR)
            connected to the analog input of the NULA MINI board.
            The program prints the measured value to the console.
            For details, connection diagram and more, check out the example documentation at: <link placeholder>

@author     Soldered Electronics
"""

"""
ADC stands for Analog to Digital Converter. Where Pin can only tell us high or low, the ADC measures the actual
voltage on a pin and gives us a number for it, which is what we need to measure a whole range of light levels.
"""
from machine import Pin, ADC
import time

"""
This is a variable to which we assign the number of the pin that we connected the photoresistor's output to.
The NULA MINI board uses analog-capable pins (ADC pins) to read varying voltages.
In this example, we will use IO5, which supports analog input.

This example also needs a 10k resistor. A photoresistor changes its resistance with light, but the board can only
measure a voltage, so we pair the two in what is called a voltage divider: the fixed resistor turns the changing
resistance into a changing voltage that the board can read.
"""
LDR_PIN = 5

"""
Here we create our ADC object, which we named "ldr". We hand it a Pin, and from then on we read the light level
through this name.
The atten setting chooses how large a voltage the converter can measure. ADC.ATTN_11DB is the widest setting, which
lets us use the full range of the photoresistor from complete darkness to bright light.
"""
ldr = ADC(Pin(LDR_PIN), atten=ADC.ATTN_11DB)

# Print a startup message to confirm that the program is running.
print("Cover or shine light on the sensor to see value changes...")

while True:

    """
    read() reads the voltage at the given analog pin and converts it into a number. Since the NULA board uses a 12-bit
    ADC, the returned value will range from 0 to 4095.
    The higher the light intensity, the lower the resistance of the photoresistor, and the higher the voltage read.
    """
    light_value = ldr.read()

    # Print the measured value to the console.
    print("Light level:", light_value)

    """
    time.sleep() is a function that starts a pause in the code, given in seconds. Half a second makes the readings
    easy to follow with your eyes. Feel free to experiment with this value.
    """
    time.sleep(0.5)
