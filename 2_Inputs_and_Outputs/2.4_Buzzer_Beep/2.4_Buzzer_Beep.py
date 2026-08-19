"""
@file       2.4_Buzzer_Beep.py
@brief      Example that shows how to generate simple sounds using a passive buzzer.
            The NULA MINI board will play a short melody by changing tone frequencies.
            For details, connection diagram and more, check out the example documentation at: <link placeholder>

@author     Soldered Electronics
"""

"""
PWM stands for Pulse Width Modulation. It switches a pin on and off very quickly, and we can choose both how fast it
switches and what fraction of the time it stays on. Feeding that fast switching into a buzzer is what makes it
produce a sound, and the switching speed is what we hear as the pitch.
"""
from machine import Pin, PWM
import time

"""
This is a variable to which we assign the number of the pin that we connected the buzzer to.
The NULA board has a pin naming logic as follows: IO5, where 5 is the number that we give to the variable.
If you wish to use a different pin, make sure you are using a IO__ marked pin.
"""
BUZZER_PIN = 5

"""
We will use two lists - one for note frequencies (in Hertz) and one for note durations.
These define a short melody that the buzzer will play. A frequency is how many times per second the buzzer moves back
and forth, and our ears hear it as the pitch of the note: the higher the number, the higher the note.
"""
melody = [262, 294, 330, 349, 392, 440, 494, 523]  # C4 to C5
note_duration = [4, 4, 4, 4, 4, 4, 4, 2]           # Quarter notes (last one is half note)

"""
Here we create our PWM object, which we named "buzzer". Creating it already claims the pin, so unlike a plain Pin we
do not set a direction for it.
"""
buzzer = PWM(Pin(BUZZER_PIN))

"""
duty_u16() sets what fraction of the time the pin stays on, as a number from 0 (always off) to 65535 (always on).
Half of that, 32768, is the even on-off switching that gives a buzzer its clearest tone, so we use it as our "sound
on" value and 0 as our "sound off" value.
"""
SOUND_ON = 32768
SOUND_OFF = 0

# Start with the buzzer silent, so it does not sound before the melody begins.
buzzer.duty_u16(SOUND_OFF)

print("Playing melody...")

"""
A for loop repeats a block of code once for every item it is given. range(len(melody)) counts from 0 up to the number
of notes in our list, so "i" ends up being the position of each note in turn, and we use it to read the matching
entry out of both lists.
"""
for i in range(len(melody)):

    """
    Musical note lengths are written as fractions: a quarter note is a quarter of a whole note. Here we turn that
    fraction into milliseconds by dividing one second by the number in the list, so a 4 becomes 250 ms and a 2
    becomes 500 ms.
    """
    duration = int(1000 / note_duration[i])

    """
    freq() sets how fast the pin switches, which is the pitch of the note, and duty_u16() then starts the sound.
    """
    buzzer.freq(melody[i])
    buzzer.duty_u16(SOUND_ON)

    # Play the note for its full length.
    time.sleep_ms(duration)

    """
    Now we stop the sound and wait a little longer before the next note. That extra silence keeps the notes from
    running into each other. Feel free to experiment with the 1.3.
    """
    buzzer.duty_u16(SOUND_OFF)
    time.sleep_ms(int(duration * 0.3))

"""
deinit() releases the pin once we are finished with it, leaving the buzzer silent for good. Without it the PWM
hardware would stay claimed even after the program ends.
"""
buzzer.deinit()
print("Melody finished!")
