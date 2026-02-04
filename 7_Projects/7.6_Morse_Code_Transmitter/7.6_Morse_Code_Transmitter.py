"""
@file		7.6_Morse_Code_Transmitter.py
@brief		A project simulating a Morse code transmitter using an LED and a buzzer. 
            The user can input text via the serial monitor, which is then transmitted in Morse code.

@author		Soldered
"""

from machine import Pin, PWM
import time

LED_PIN = 3          
BUZZER_PIN = 4

# Unit time in seconds (dot length)
UNIT = 0.12

led = Pin(LED_PIN, Pin.OUT)
led.value(0)  # Turn off initially

buzz = PWM(Pin(BUZZER_PIN))
buzz.freq(800)
buzz.duty(0) # Mute initially

def buzzer_on():
    buzz.duty(512)

def buzzer_off():
    buzz.duty(0)

# Morse code map (International)
MORSE = {
    'A': '.-',    'B': '-...',  'C': '-.-.', 'D': '-..',  'E': '.',
    'F': '..-.',  'G': '--.',   'H': '....', 'I': '..',   'J': '.---',
    'K': '-.-',   'L': '.-..',  'M': '--',   'N': '-.',   'O': '---',
    'P': '.--.',  'Q': '--.-',  'R': '.-.',  'S': '...',  'T': '-',
    'U': '..-',   'V': '...-',  'W': '.--',  'X': '-..-', 'Y': '-.--',
    'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.'
}

# Morse signaling function for 'dot'
def dot():
    led.value(1)
    buzzer_on()
    time.sleep(UNIT)         # dot = 1 unit
    led.value(0)
    buzzer_off()

    time.sleep(UNIT)         

# Morse signaling function for 'dash'
def dash():
    led.value(1)
    buzzer_on()
    time.sleep(UNIT * 3)     # dash = 3 units
    led.value(0)
    buzzer_off()
    time.sleep(UNIT)         

# Send a single character in Morse code
def send_character(morse_code):
    # morse_code: string of '.' and '-'
    for _, s in enumerate(morse_code):
        if s == '.':
            dot()
        elif s == '-':
            dash()
    # After character, wait additional 2 units (since last dot/dash already waited 1)
    time.sleep(UNIT * 2)


def send_text(msg):
    msg = msg.strip()
    for _, ch in enumerate(msg):
        if ch == ' ':
            # Word gap: 7 units total, previous character added 3 units
            time.sleep(UNIT * 4)  # send_character already added 3 units total (1 after last symbol + 2)
            continue
        code = MORSE.get(ch.upper())
        if code:
            send_character(code)
        else:
            # Undefined char -> short pause and continue
            time.sleep(UNIT * 3)

# Main loop
print("Morse transmitter ready. Type a message and press Enter.")
try:
    while True:
        # Read a line from serial input
        try:
            line = input()
        except Exception:
            line = ''
        if not line:
            continue
        print("Sending:", line)
        # Transmit the input text as Morse code
        send_text(line)
        print("Done.")
except KeyboardInterrupt:
    print("Stopped by user")
finally:
    led.value(0)
    buzzer_off()
