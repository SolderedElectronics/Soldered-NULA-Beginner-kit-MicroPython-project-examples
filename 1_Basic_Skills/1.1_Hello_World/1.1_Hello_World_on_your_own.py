"""
@file       1.1_Hello_World_on_your_own.py
@brief      Variation of the 1.1 Hello World example that prints "Hello, World!" once a second for as long as the
            board has power.
            For details, connection diagram and more, check out the example documentation at: <link placeholder>

@author     Soldered Electronics
"""

import time  # brings in the module that knows how to wait

"""
print() sends text from the board back to your computer over the USB cable. Whatever you print appears in the
console of the editor you are using, which for MicroPython is usually Thonny. This is the simplest way for a
board to tell you what it is doing, and you will use it in almost every example from here on.
There is nothing to set up first. The board is already talking to your computer, so a single line is enough.
"""
# while True: repeats the indented lines below it for as long as the board runs
while True:
    print("Hello, World!")

    # Wait one second before the next pass, or the lines would pour out too fast to read
    time.sleep(1)
