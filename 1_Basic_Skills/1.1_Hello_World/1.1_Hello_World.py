"""
@file       1.1_Hello_World.py
@brief      Example that shows basic functionality of the serial console, writing data only.
            For details, connection diagram and more, check out the example documentation at: <link placeholder>

@author     Soldered
"""

"""
print() sends text from the board back to your computer over the USB cable. Whatever you print appears in the
console of the editor you are using, which for MicroPython is usually Thonny. This is the simplest way for a
board to tell you what it is doing, and you will use it in almost every example from here on.
Unlike Arduino, MicroPython does not need the serial connection to be opened first. The board is already talking
to your computer, so a single line is enough.
"""
print("Hello, World!")
