"""
@file     2.3_Photoresistor_Analog_Read.py
@brief    Example that demonstrates how to read analog values from a photoresistor (LDR)
          using an input pin.
          
@author   Soldered
"""

# Import Pin and ADC modules to read analog values from photoresistor
from machine import Pin, ADC
import time

# Define pin object used for photoresistor
LDR_PIN = 5

# Create ADC object for photoresistor pin
ldr = ADC(Pin(LDR_PIN))

# Infinite loop to continuously read sensor values
while True:
    # Read the analog value from the photoresistor
    ldr_value = ldr.read()
    
    # Print the LDR value to the console
    print(f"LDR Value: {ldr_value}")
    
    # Pause the program briefly to allow some time for CPU
    time.sleep(0.5)

