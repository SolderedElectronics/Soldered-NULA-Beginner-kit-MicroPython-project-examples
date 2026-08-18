"""
@file       7.2_Mini_piano.py
@brief      Project that turns four buttons and a passive buzzer into a small piano. Each button has its own
            frequency, and pressing it plays that note for as long as you hold the button down.
            It builds on the button reading from section 2.1 and the buzzer from section 2.4.
            For details, connection diagram and more, check out the example documentation at: <link placeholder>

@author     Soldered
"""

"""
PWM switches a pin on and off very quickly, and feeding that into a buzzer is what makes it produce a sound. The
switching speed is what we hear as the pitch. This is how MicroPython does what the tone() function does in Arduino.
"""
from machine import Pin, PWM
import time

"""
This is a variable to which we pass the number of pin that we had connected the buzzer to.
The NULA board has a pin naming logic as follows: IO18, where 18 is the number that we give to the variable.
If you wish to use a different pin, make sure you are using a IO__ marked pin.
"""
BUZZER_PIN = 18

"""
These are the variables to which we pass the numbers of pins that we had connected the four BUTTONS to. Each button
gets a pin of its own, because the board has to be able to tell them apart.
"""
BTN1 = 2
BTN2 = 3
BTN3 = 4
BTN4 = 5

"""
These are the frequencies of the four notes, in Hertz. A frequency is how many times per second the buzzer moves back
and forth, and it is what our ears hear as the pitch of the sound: the higher the number, the higher the note.
The names come from the musical scale, where C4 is the C in the middle of a piano keyboard. Feel free to experiment
with these values, or look up the frequencies of other notes and build your own scale.
"""
NOTE_C4 = 262
NOTE_D4 = 294
NOTE_E4 = 330
NOTE_F4 = 349

"""
Here we create our four Pin objects for the buttons. Pin.IN tells the board that these pins should read a value
instead of writing one, and Pin.PULL_UP switches on a resistor inside the chip that ties each pin to 3.3V while its
button is released. That means a pin reads high (1) when its button is up and low (0) while it is pressed.
"""
btn1 = Pin(BTN1, Pin.IN, Pin.PULL_UP)
btn2 = Pin(BTN2, Pin.IN, Pin.PULL_UP)
btn3 = Pin(BTN3, Pin.IN, Pin.PULL_UP)
btn4 = Pin(BTN4, Pin.IN, Pin.PULL_UP)

"""
Here we create our PWM object for the buzzer. duty_u16() sets what fraction of the time the pin stays on, as a number
from 0 (always off) to 65535 (always on). Half of that is the even on-off switching that gives a buzzer its clearest
tone, so we use it as our "sound on" value and 0 as our "sound off" value.
"""
buzzer = PWM(Pin(BUZZER_PIN))
SOUND_ON = 32768
SOUND_OFF = 0

# Start with the buzzer silent, so it makes no noise before any button is pressed.
buzzer.duty_u16(SOUND_OFF)


def play_note(frequency):
    """
    This is a function we wrote ourselves. It starts a note and leaves it playing.
    freq() sets how fast the pin switches, which is the pitch, and duty_u16() then starts the sound.
    """
    buzzer.freq(frequency)
    buzzer.duty_u16(SOUND_ON)


def stop_note():
    """
    This function stops whatever sound the buzzer was making, which is what makes the note stop as soon as you let go
    of the button.
    """
    buzzer.duty_u16(SOUND_OFF)


while True:

    """
    value() is a function that reads the value from a pin, either 1 (high) or 0 (low). Because of the pull-up
    resistors, a pressed button reads 0.
    Notice the "elif" chain: the board checks the buttons in order and stops at the first one it finds pressed, so
    pressing two buttons at once plays only the note that comes first in this list.
    """
    if btn1.value() == 0:
        play_note(NOTE_C4)
    elif btn2.value() == 0:
        play_note(NOTE_D4)
    elif btn3.value() == 0:
        play_note(NOTE_E4)
    elif btn4.value() == 0:
        play_note(NOTE_F4)
    else:

        # If none of the buttons is pressed we end up here, and the buzzer goes silent.
        stop_note()

    """
    time.sleep_ms() pauses the program for the given number of milliseconds. This very short pause gives the button
    contacts a moment to settle, which stops a single press from being read as several. Section 2.2 explains this in
    detail under the name debouncing.
    """
    time.sleep_ms(50)
