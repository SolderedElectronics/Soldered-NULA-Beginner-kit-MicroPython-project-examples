"""
@file       7.8_LED_Traffic_Light.py
@brief      Project that simulates a traffic light with three LEDs, running through green, blinking green, orange,
            red and red together with orange, just like the lights on many European roads.
            It introduces the finite state machine, or FSM, which is a very common way of writing programs that move
            through a fixed series of steps without ever pausing the program to wait.
            For details, connection diagram and more, check out the example documentation at: <link placeholder>

@author     Soldered
"""

from machine import Pin
import time

"""
These are the variables to which we pass the numbers of pins that we had connected the three LEDs to.
The NULA board has a pin naming logic as follows: IO4, where 4 is the number that we give to the variable.
If you wish to use a different pin, make sure you are using a IO__ marked pin.

Remember that every one of these LEDs needs its own 330 Ohm resistor in series with it. That resistor limits how much
current flows, and without it an LED draws more than it is built for and can be damaged.
"""
LED_GREEN = 4
LED_ORANGE = 3
LED_RED = 2

"""
These give names to a fixed set of values. Without them we would have to remember that state 0 means green and state 3
means red, and a mistake there would be very easy to make and very hard to spot. With them we can write GREEN and RED
instead, and the program reads almost like a description of a real traffic light.
Each of these names is one state that our traffic light can be in, and it can only ever be in one of them at a time.
"""
GREEN = 0
GREEN_BLINK = 1
ORANGE = 2
RED = 3
RED_ORANGE = 4

"""
Here we create our three Pin objects. Pin.OUT tells the board that these pins should write a value instead of reading
one, since all three of them drive an LED.
"""
green_led = Pin(LED_GREEN, Pin.OUT)
orange_led = Pin(LED_ORANGE, Pin.OUT)
red_led = Pin(LED_RED, Pin.OUT)

"""
This variable holds the state we are in right now. Together with the two below it, it is the whole memory of our state
machine: "last_change" remembers the moment we entered the current state, and "state_duration" holds how long we mean to
stay in it. That is all a finite state machine needs: where am I, since when, and for how long.
time.ticks_ms() returns the number of milliseconds passed since the board was powered on, so storing it now means "the
green state began at this moment". The duration says we mean to stay green for 5000 milliseconds, which is five seconds.
"""
state = GREEN
last_change = time.ticks_ms()
state_duration = 5000

"""
These three variables are only used by the blinking green state. "green_on" remembers whether the green LED is currently
lit, "BLINK_INTERVAL" is how long it stays that way before flipping, and "last_blink" remembers when it last flipped.
Feel free to experiment with the interval to make the blinking faster or slower.
"""
green_on = True
BLINK_INTERVAL = 400
last_blink = time.ticks_ms()

# Print out the initial message so we know that the program started successfully.
print("Traffic Light Example started!")
print("State: GREEN")

while True:

    """
    We read the clock once at the top of the loop and use that one value everywhere below, which keeps all the
    comparisons in this pass consistent with each other.
    """
    now = time.ticks_ms()

    """
    Below, each state gets its own block, and only the block belonging to the current state runs. Notice that every block
    does the same two things: it sets the LEDs the way this state wants them, and then it checks whether its time is up.
    If it is, it names the next state, remembers the current moment as the new starting point, and sets how long the next
    state should last. That pattern repeating five times is the entire state machine.
    """
    if state == GREEN:

        # Green on, everything else off.
        green_led.value(1)
        orange_led.value(0)
        red_led.value(0)

        # After five seconds, move on to the blinking green state and give it three seconds.
        if time.ticks_diff(now, last_change) >= state_duration:
            state = GREEN_BLINK
            last_change = now
            state_duration = 3000

            """
            Here we set the blinking up before we hand over to it. Without these two lines the blink would carry on
            from wherever it left off the previous time around the cycle, so the green LED could enter this state
            switched off and the first flash would come at the wrong moment.
            """
            green_on = True
            last_blink = now

            print("State: GREEN_BLINK")

    elif state == GREEN_BLINK:

        """
        Here we leave the green LED alone, because the blinking below is what decides whether it is on or off. The other
        two stay off.
        """
        orange_led.value(0)
        red_led.value(0)

        """
        This is the blinking itself. Every time the interval has passed we flip green_on to its opposite value with the
        "not" operator and write the new value to the pin. Because this runs on the clock rather than on a pause, the
        state machine above keeps working the whole time the LED is blinking.
        """
        if time.ticks_diff(now, last_blink) >= BLINK_INTERVAL:
            green_on = not green_on
            green_led.value(1 if green_on else 0)
            last_blink = now

        # After three seconds of blinking, move on to orange and give it two seconds.
        if time.ticks_diff(now, last_change) >= state_duration:
            state = ORANGE
            last_change = now
            state_duration = 2000
            print("State: ORANGE")

    elif state == ORANGE:

        # Orange on, everything else off.
        green_led.value(0)
        orange_led.value(1)
        red_led.value(0)

        # After two seconds, move on to red and give it five seconds.
        if time.ticks_diff(now, last_change) >= state_duration:
            state = RED
            last_change = now
            state_duration = 5000
            print("State: RED")

    elif state == RED:

        # Red on, everything else off.
        green_led.value(0)
        orange_led.value(0)
        red_led.value(1)

        # After five seconds, move on to red together with orange and give it two seconds.
        if time.ticks_diff(now, last_change) >= state_duration:
            state = RED_ORANGE
            last_change = now
            state_duration = 2000
            print("State: RED_ORANGE")

    elif state == RED_ORANGE:

        # Red and orange lit at the same time, which on many European traffic lights is the warning that green is coming.
        green_led.value(0)
        orange_led.value(1)
        red_led.value(1)

        # After two seconds we are back at the start, and the whole cycle begins again.
        if time.ticks_diff(now, last_change) >= state_duration:
            state = GREEN
            last_change = now
            state_duration = 5000
            print("State: GREEN")

    # A very short pause leaves the processor a moment to handle its own background work.
    time.sleep_ms(10)
