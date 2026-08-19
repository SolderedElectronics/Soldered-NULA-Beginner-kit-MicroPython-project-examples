"""
@file       4.2_Auto_Scroll_Text.py
@brief      Example that shows how to automatically scroll text on a 16x2 LCD.
            The LCD is controlled using the Soldered LCD driver.
            This example demonstrates how to use scrollDisplayLeft() to move text across the screen.
            For details, connection diagram and more, check out the example documentation at: <link placeholder>

@author     Soldered Electronics
"""

# I2C is what the Qwiic connector carries, and the display is a Qwiic module.
from machine import I2C, Pin

# The Soldered driver for the LCD display, found in the lib folder of this repository.
from LCD import LCD_I2C
import time

"""
Here we set up the I2C connection. On the NULA MINI, I2C uses IO6 for the data line (SDA) and IO7 for the clock line
(SCL), which are the pins the Qwiic connector is wired to.
"""
i2c = I2C(0, scl=Pin(7), sda=Pin(6))

"""
Here we create our display object, which we named "lcd", and hand it the I2C connection.
The display is 16 characters wide and 2 rows tall.
"""
lcd = LCD_I2C(i2c)

"""
Create a message that will scroll across the display. The spaces at the beginning and the end leave a small gap, so
the text does not run straight into itself as it travels.
"""
message = " Hello from NULA MINI! "

"""
The speed of scrolling in milliseconds. Higher number = slower scroll.
Feel free to experiment with this value.
"""
SCROLL_DELAY_MS = 300

# begin() starts the communication and prepares the display. It has to come before anything else.
lcd.begin()

# backlight() turns on the light behind the screen. It comes after begin(), which would otherwise switch it back off.
lcd.backlight()

# Print the message once. Only the visible part will show initially.
lcd.print(message)

while True:

    """
    scrollDisplayLeft() shifts everything already on the screen one position to the left. We never print the message
    again, we only keep moving it, and doing that over and over is what creates the moving effect.
    """
    lcd.scrollDisplayLeft()

    """
    time.sleep_ms() pauses the program for the given number of milliseconds. This is what controls the scrolling
    speed: a longer wait between movements means slower scrolling.
    """
    time.sleep_ms(SCROLL_DELAY_MS)
