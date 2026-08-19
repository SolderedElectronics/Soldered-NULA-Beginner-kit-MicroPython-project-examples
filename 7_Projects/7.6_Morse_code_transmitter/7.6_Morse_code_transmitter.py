"""
@file       7.6_Morse_code_transmitter.py
@brief      Project that turns text you type into the console into Morse code and blinks it out on an LED.
            Morse code represents every letter as a pattern of short and long signals, called dots and dashes.
            Along the way the example introduces three new ideas: reading text you type in, storing a lookup table,
            and writing your own functions to keep a longer program readable.
            For details, connection diagram and more, check out the example documentation at: <link placeholder>

@author     Soldered Electronics
"""

from machine import Pin
import time

"""
This is a variable to which we pass the number of pin that we had connected the LED to.
The NULA board has a pin naming logic as follows: IO2, where 2 is the number that we give to the variable.
If you wish to use a different pin, make sure you are using a IO__ marked pin.

Remember that the LED needs a 330 Ohm resistor in series with it. That resistor limits how much current flows, and
without it the LED draws more than either it or the pin is built for, so both can be damaged.
"""
LED_PIN = 2

"""
Morse code does not measure its signals in milliseconds but in units, and every other duration is a multiple of one
unit. That is why only the first value below is a real number and the rest are calculated from it: change DOT_DURATION
alone and the whole transmission speeds up or slows down while staying correct Morse.
The standard proportions are a dash three units long, one unit of silence between the dots and dashes of a letter,
three units between letters, and seven units between words.
"""
DOT_DURATION = 300
DASH_DURATION = DOT_DURATION * 3
SYMBOL_GAP = DOT_DURATION
LETTER_GAP = DOT_DURATION * 3
WORD_GAP = DOT_DURATION * 7

"""
This is our lookup table: it pairs every character we can send with the dots and dashes that stand for it. A lookup
table is simply a list we search through instead of writing out dozens of if statements, and it has the nice property
that adding a new character means adding one line here and changing nothing else.
In Python this kind of table is called a dictionary, and looking something up in it is as simple as naming the
character you want.
The last entry pairs a space with a space, which is how we recognise the gap between two words.
"""
MORSE_TABLE = {
    "A": ".-",    "B": "-...",  "C": "-.-.",  "D": "-..",   "E": ".",
    "F": "..-.",  "G": "--.",   "H": "....",  "I": "..",    "J": ".---",
    "K": "-.-",   "L": ".-..",  "M": "--",    "N": "-.",    "O": "---",
    "P": ".--.",  "Q": "--.-",  "R": ".-.",   "S": "...",   "T": "-",
    "U": "..-",   "V": "...-",  "W": ".--",   "X": "-..-",  "Y": "-.--",
    "Z": "--..",
    "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....",
    "6": "-....", "7": "--...", "8": "---..", "9": "----.", "0": "-----",
    " ": " ",
}

"""
Here we create our Pin object for the LED. Pin.OUT tells the board that this pin should write a value instead of
reading one. Right after that we write 0 to it, so the LED starts out switched off.
"""
led = Pin(LED_PIN, Pin.OUT)
led.value(0)


def get_morse_code(character):
    """
    This is a function we wrote ourselves. It takes a character and hands back the dots and dashes that stand for it.
    upper() turns a lowercase letter into an uppercase one, so that typing "sos" works just as well as "SOS".
    get() looks the character up in our table, and the second value we give it is what comes back when the character is
    not in the table at all. Here that is empty text, which the transmitting function below simply skips over.
    """
    return MORSE_TABLE.get(character.upper(), "")


def blink_symbol(symbol):
    """
    This function blinks out a single dot or dash. It picks the right duration for the symbol it was given, switches the
    LED on for exactly that long, and then switches it off and waits one more unit, which is the silence that separates
    one symbol from the next.
    """
    if symbol == ".":
        duration = DOT_DURATION
    else:
        duration = DASH_DURATION

    led.value(1)
    time.sleep_ms(duration)
    led.value(0)
    time.sleep_ms(SYMBOL_GAP)


def transmit_text(text):
    """
    This function transmits a whole piece of text. It does the work twice over: first it prints the translation to the
    console so you can read along, and then it blinks the same thing out on the LED.
    """
    print()
    print("--- TRANSMITTING ---")
    print("Text:  ", text)

    """
    This first loop walks through the text one character at a time. For each of them we look up the code and collect it,
    and join() then glues the collected pieces together with a space between them.
    """
    codes = []
    for character in text:
        codes.append(get_morse_code(character))
    print("Morse: ", " ".join(codes))
    print("--------------------")

    """
    This second loop walks through the very same text again, but this time it blinks instead of printing.
    A space is not blinked at all, it is a pause, so when we find one we wait a word gap and skip the rest of this pass
    with continue. Otherwise the inner loop blinks the symbols of the letter one by one, and once they are done we wait
    a letter gap before moving on to the next letter.
    """
    for character in text:
        code = get_morse_code(character)
        if code == " ":
            time.sleep_ms(WORD_GAP)
            continue
        for symbol in code:
            blink_symbol(symbol)
        time.sleep_ms(LETTER_GAP)

    print()
    print("Transmission complete!")
    print()


# Invite the user to type something. Type into the console of your editor and press Enter.
print("Enter text to send via Morse code:")

while True:

    """
    input() waits until you type a line and press Enter, then hands us what you typed. This is the simplest way of
    getting information from the computer into the board, and it is the counterpart of the print() we have been using
    in the other direction all along.
    """
    text = input()

    """
    strip() removes any stray spaces or leftover line endings from both ends, which is worth doing because different
    systems end their lines slightly differently.
    """
    text = text.strip()

    """
    Finally we check that something is actually left after stripping, so that pressing Enter on an empty line does not
    start a transmission, and hand the text over to our own function above.
    """
    if len(text) > 0:
        transmit_text(text)
