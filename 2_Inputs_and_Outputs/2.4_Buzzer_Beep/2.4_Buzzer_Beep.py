"""
@file		2.4_Buzzer_Beep.py
@brief		Example demonstrating how to use PWM to produce sound with a buzzer.

@author		Soldered
"""

# Import Pin and PWM modules to control the buzzer
from machine import Pin, PWM
import time

# Create PWM object for buzzer on pin 5
buzzer = PWM(Pin(5))

# Define notes and their frequencies (in Hz)
C4 = 262
D4 = 294
E4 = 330
F4 = 349
G4 = 392
A4 = 440

# Define a melody as a list of note frequencies
melody = [C4, D4, E4, F4, G4, A4, G4, F4, E4, D4, C4]

# Playback duration for each note (ms)
duration = 200

# Loop through the melody and play each note with a small pause in between
for note in melody:
    buzzer.freq(note)           # Set buzzer frequency based on the note
    buzzer.duty(512)            # 50% duty (sound on)
    time.sleep_ms(duration)     # Play note for defined duration
    buzzer.duty(0)              # 0% duty (sound off)
    time.sleep_ms(150)          # Short pause between notes

# Disable the PWM output for the buzzer
buzzer.deinit()
