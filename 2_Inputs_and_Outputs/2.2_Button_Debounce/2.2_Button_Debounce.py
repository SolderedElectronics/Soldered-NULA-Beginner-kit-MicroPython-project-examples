"""
@file       2.2_Button_Debounce.py
@brief      Example that shows how to toggle LED light with a press of a button.
            In this example we will be using a button reading technique called debouncing. This technique gives us
            an easy way to stabilize the button readings.
            For details, connection diagram and more, check out the example documentation at: <link placeholder>

@author     Soldered
"""

from machine import Pin
import time

"""
This is a variable to which we pass the number of pin that we had connected the BUTTON to.
The NULA board has a pin naming logic as follows: IO19, where 19 is the number that we give to the variable.
If you wish to use a different pin, make sure you are using a IO__ marked pin.
"""
BUTTON_PIN = 19

"""
This is a variable to which we pass the number of pin that we had connected the LED to.

Remember that the LED needs a 330 Ohm resistor in series with it. That resistor limits how much current flows, and
without it the LED draws more than either it or the pin is built for, so both can be damaged.
"""
LED_PIN = 4

"""
Here we create our two Pin objects. The button is set to Pin.IN because we read it, with Pin.PULL_UP switching on a
resistor inside the chip that ties the pin to 3.3V while the button is released, so the button only has to connect the
pin to GND. The LED is set to Pin.OUT because we write to it.
"""
btn = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
led = Pin(LED_PIN, Pin.OUT)

"""
Those are the variables used for button debouncing. To learn more about button debouncing, check out our example
documentation at: <link placeholder>
"led_state" remembers whether the LED is currently on, "last_state" remembers what the button read the last time we
looked, and "last_change_ms" remembers when that reading last changed.
"""
led_state = False
last_state = 1
last_change_ms = 0
DEBOUNCE_MS = 25

# Make sure the LED starts out switched off, so the state we remember matches what you actually see.
led.value(0)

while True:

    # value() is a function that reads the value from our pin, either 1 (high) or 0 (low).
    reading = btn.value()

    """
    time.ticks_ms() is a function that returns the number of milliseconds passed since the board was powered on.
    In this example, we use this function to check if the debouncing period has finished.
    This counter eventually wraps around back to zero, which is why we never compare two of these numbers directly
    and always use time.ticks_diff() to work out the difference between them.
    """
    now = time.ticks_ms()

    """
    This is our debouncing logic, we check if the button reading has changed and if enough time has passed so that we
    don't get false readings because of the noise in the signal. A mechanical button does not switch cleanly: its
    contacts bounce for a few milliseconds, and without this check a single press would be counted several times.
    """
    if reading != last_state and time.ticks_diff(now, last_change_ms) > DEBOUNCE_MS:
        last_change_ms = now

        """
        As we are using the pull-up method for reading the button, the readings are the other way around from what
        you might expect: the pin reads high while the button is released and low while it is pressed. So we need to
        toggle the LED when the button state goes from high to low.
        """
        if last_state == 1 and reading == 0:

            # We toggle the led_state. The "not" operator flips True into False and False into True.
            led_state = not led_state

            # We turn the LED on or off depending on the current led_state.
            if led_state:
                led.value(1)
            else:
                led.value(0)

            print("Button pressed, toggling LED")

        last_state = reading

    # A very short pause leaves the processor a moment to handle its own background work.
    time.sleep_ms(10)
