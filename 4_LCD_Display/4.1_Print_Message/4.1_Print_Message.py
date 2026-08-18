"""
@file       4.1_Print_Message.py
@brief      Example that shows how to display a message on an LCD screen.
            The LCD is controlled using the Soldered LCD driver.
            This example demonstrates the basics of initializing the display and printing text.
            For details, connection diagram and more, check out the example documentation at: <link placeholder>

@author     Soldered
"""

"""
I2C is a way for several devices to talk to the board over just two wires, and it is what the Qwiic connector carries.
We need it here because the display is a Qwiic module.
"""
from machine import I2C, Pin

"""
The Soldered driver for the LCD display. It lives in the lib folder of this repository, so copy the whole lib folder
onto your board, otherwise MicroPython will not be able to find it.
"""
from LCD import LCD_I2C

"""
Here we set up the I2C connection. The two pins are fixed by the board: on the NULA MINI, I2C uses IO6 for the data
line (SDA) and IO7 for the clock line (SCL), which are exactly the pins the Qwiic connector is wired to.
Unlike Arduino, MicroPython does not find these on its own, so we always name them.
"""
i2c = I2C(0, scl=Pin(7), sda=Pin(6))

"""
Here we create our display object, which we named "lcd". An object is our way of talking to the display: every
function we call on it, we call through this name. We hand it the I2C connection we just made.
The display in this kit is 16 characters wide and 2 rows tall, which is where the name 16x2 comes from.
"""
lcd = LCD_I2C(i2c)

"""
begin() starts the communication and prepares the display for use. It has to come first, before anything else we ask
the display to do.
"""
lcd.begin()

"""
backlight() turns on the light behind the screen, without which the text is very hard to read. Note that this has to
come after begin(), because begin() resets the display and would switch the light back off.
"""
lcd.backlight()

# clear() wipes anything that was left on the screen from before, so we start from a clean display.
lcd.clear()

"""
setCursor() chooses where the next text will appear. The first number is the column and the second is the row, and
both start counting at zero, so (0, 0) is the top left corner.
print() then writes our text starting at that position.
"""
lcd.setCursor(0, 0)
lcd.print("Hello, NULA!")

"""
Move to the second line and print another message. (0, 1) means column zero of row one, which is the start of the
second line.
Keep in mind that this display fits exactly 16 characters per row, so anything longer is simply cut off at the edge.
Count the characters of your own messages before printing them.
"""
lcd.setCursor(0, 1)
lcd.print("Let's start!")

"""
And that is all. Unlike the earlier examples there is no while True loop here, because nothing needs to happen over
and over: the message stays on the screen until the board is reset or powered off.
"""
