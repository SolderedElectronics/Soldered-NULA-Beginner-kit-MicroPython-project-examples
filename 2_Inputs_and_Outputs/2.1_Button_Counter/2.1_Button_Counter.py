"""
@file       2.1_Button_Counter.py
@brief      Example that shows how to increase a counter each time a button is pressed.
            This example does NOT use any debouncing or signal stabilization.
            For details, connection diagram and more, check out the example documentation at: <link placeholder>

@author     Soldered Electronics
"""

# The machine module holds everything that talks to the hardware, and Pin controls a single pin.
from machine import Pin
import time

"""
This is a variable to which we pass the number of pin that we had connected the BUTTON to.
The NULA board has a pin naming logic as follows: IO19, where 19 is the number that we give to the variable.
If you wish to use a different pin, make sure you are using a IO__ marked pin.
"""
BUTTON_PIN = 19

"""
Here we create our Pin object, which we named "btn". Pin.IN tells the board that this pin should read a value instead
of writing one.
Pin.PULL_UP switches on a resistor inside the chip that gently ties the pin to 3.3V. Without it the pin would be
floating, meaning it is connected to nothing and picks up random noise, and the board would read presses that never
happened. Because the resistor holds the pin high, the button only has to connect the pin to GND, so no extra parts
are needed on the breadboard.
"""
btn = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

"""
This variable holds the value of our counter.
Each time the button is pressed, the counter value will increase by one.
"""
counter = 0

# Print out the initial message so we know that the program started successfully.
print("Button Counter Example started!")
print("Press the button to increase the counter...")

# A while True loop repeats forever, so the code inside it keeps running until we stop the program.
while True:

    """
    value() is a function that reads the value from our pin, either 1 (high) or 0 (low).
    Note that the reading is the other way around from what you might expect. The pull-up resistor holds the pin at
    3.3V while the button is released, so we read 1, and pressing the button connects the pin to GND so we read 0.
    A button wired this way is called active low.
    """
    reading = btn.value()

    """
    If the button is pressed, increase the counter by one and print it to the console.
    Since this version does not include debouncing, multiple counts may appear for a single press.
    """
    if reading == 0:
        counter += 1
        print("Counter:", counter)

        """
        Wait for the button to be released before allowing another count.
        This prevents the counter from increasing too quickly while the button is still held down.
        """
        while btn.value() == 0:
            # Wait until the button is released
            time.sleep_ms(10)

    """
    time.sleep_ms() pauses the program for the given number of milliseconds. A very short pause here leaves the
    processor a moment to handle its own background work instead of spending every cycle checking the button.
    """
    time.sleep_ms(10)
