"""
@file		7.1_Piano_Project.py
@brief		A project that combines multiple components to build a fun, interactive piano.

@author		Soldered
"""

# Import necessary modules
from machine import Pin, PWM
import time

# Pin configurations
BUZZER_PIN = 2
BUTTON_PINS = [3, 4, 5, 18, 19]  # 5 buttons

# Notes for each button (you can adjust as needed)
NOTES = {
    3: 262,   # C4
    4: 294,   # D4
    5: 330,   # E4
    18: 349,  # F4
    19: 392   # G4
}

# Setup PWM for buzzer
buzzer = PWM(Pin(BUZZER_PIN))
buzzer.duty(0)

# Setup buttons with pull-ups
buttons = {}
for pin_num in BUTTON_PINS:
    buttons[pin_num] = Pin(pin_num, Pin.IN, Pin.PULL_UP)

# Play note function
def play_note(freq):
    buzzer.freq(freq)
    buzzer.duty(512)  # 50% duty

# Stop buzzer
def stop_note():
    buzzer.duty(0)

# Main loop
while True:
    pressed_any = False
    # Check each button
    for pin_num, btn in buttons.items():
        if not btn.value():  # button pressed (active low)
            # Get the frequency for the pressed button
            freq = NOTES[pin_num]
            # Play the note
            play_note(freq)
            print("PLAY", freq, "Hz")
            # Set the flag for pressed button
            pressed_any = True
            # Exit the loop to avoid multiple notes at once
            break
 
    # If no button is pressed, mute the buzzer
    if not pressed_any:
        stop_note()

    # Small delay to not overload the CPU
    time.sleep_ms(20)
