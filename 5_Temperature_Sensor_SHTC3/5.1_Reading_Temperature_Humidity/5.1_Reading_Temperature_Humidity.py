"""
@file		5.1_Reading_Temperature_Humidity.py
@brief		Example that shows how to use SHTC3 Temp & Humidity sensor to measure
            values and display them on 16x2 LCD display in real time.

@author		Soldered
"""

# Import Pin and I2C to initialize communications with external LCD and SHTC3 modules
from machine import Pin, I2C
# Import LCD display module
from LCD import LCD_I2C
# Import SHTC3 sensor module
from SHTC3 import SHTC3
import time

# Set up I2C connection with SHTC3 sensor using custom I2C pins
i2c_shtc3 = I2C(0, scl=Pin(3), sda=Pin(4))
# Initialize sensor module
shtc3 = SHTC3(i2c_shtc3)

# Set up I2C connection with LCD display using default I2C pins
i2c_lcd = I2C(0, scl=Pin(7), sda=Pin(6))
# Initialize display module
lcd = LCD_I2C(i2c_lcd)

# Turn on the backlight of the LCD
lcd.backlight()
# Start communication with the LCD over I2C
lcd.begin()

# Function to format string to exactly 16 characters
def format_lcd_text(text):
    return (text + " " * 16)[:16]

# Infinite loop
while True:
    # Sample the values before reading them
    shtc3.sample()
    # Read the temperature and humidity values that were just sampled
    temperature = shtc3.readTemperature()
    humidity = shtc3.readHumidity()
    print(f"{temperature}, {humidity}")
    # Move cursor to first character in first row
    lcd.setCursor(0, 0)
    # Print temperature ('\xDFC' prints degree symbol on this LCD)
    lcd.print(format_lcd_text("Temp: {:.1f}\xDFC".format(temperature)))
    # Move cursor to first character in second row
    lcd.setCursor(0, 1)
    # Print humidity
    lcd.print(format_lcd_text("Hum: {:5.1f}%".format(humidity)))
    # Pause the program for two seconds
    time.sleep(2.0)
