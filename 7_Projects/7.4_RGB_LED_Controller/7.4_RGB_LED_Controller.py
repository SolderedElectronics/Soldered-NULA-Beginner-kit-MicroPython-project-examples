"""
@file       7.4_RGB_LED_Controller.py
@brief      Project that uses a photoresistor to set the colour of an RGB LED. As the light in the room changes,
            the colour slides from red in darkness, through green and blue, all the way to white in bright light.
            It builds on the photoresistor from section 2.3 and the LED brightness control from section 3.2, and
            shows how one sensor reading can drive three outputs at the same time.
            For details, connection diagram and more, check out the example documentation at: <link placeholder>

@author     Soldered
"""

"""
ADC measures the actual voltage on a pin and gives us a number for it, which is how we read the light level. PWM
switches a pin on and off very quickly, which is how we set a brightness instead of only on or off.
"""
from machine import Pin, ADC, PWM
import time

"""
This is a variable to which we pass the number of pin that we had connected the photoresistor's output to. Because we
need to read a whole range of values here and not only high or low, this has to be a pin that supports analog input.
The NULA board has a pin naming logic as follows: IO5, where 5 is the number that we give to the variable.

This example also needs a 10k resistor. A photoresistor changes its resistance with light, but the board can only
measure a voltage, so we pair the two in what is called a voltage divider: the fixed resistor turns the changing
resistance into a changing voltage that the board can read.
"""
LDR_PIN = 5

"""
These are the variables to which we pass the numbers of pins that we had connected the three colour channels of the
RGB LED to. An RGB LED is really three LEDs in one package, one red, one green and one blue, and by lighting them at
different strengths we can mix any colour we like. All three are driven with PWM, which is what lets us set a
brightness rather than only switching them on and off.

Remember that each of the three colour channels needs its own 330 Ohm resistor in series with it. An RGB LED counts as
three LEDs, so it takes three resistors, and without them the channels draw more current than either they or the pins
are built for.
"""
RED_PIN = 2
GREEN_PIN = 3
BLUE_PIN = 4

"""
This is how fast the PWM pins switch on and off. 1000 times per second is far quicker than our eyes can follow, so we
see steady colours instead of flickering.
"""
PWM_FREQ = 1000

"""
These two variables split the light range into three equal parts, which is what gives us our three colour transitions.
The photoresistor readings run from 0 to 4095, and 4095 divided by three is 1365, so the first part ends there and the
second one ends at twice that. Feel free to experiment with these values to move the colour changes to different light
levels.
"""
FIRST_THIRD = 1365
SECOND_THIRD = 2730

"""
Here we create our ADC object, which we named "ldr". The atten setting chooses how large a voltage the converter can
measure, and ADC.ATTN_11DB is the widest setting, which lets us use the full range of the photoresistor.
"""
ldr = ADC(Pin(LDR_PIN), atten=ADC.ATTN_11DB)

"""
Here we create one PWM object for each colour channel, all at the same switching speed.
"""
pwm_r = PWM(Pin(RED_PIN), freq=PWM_FREQ)
pwm_g = PWM(Pin(GREEN_PIN), freq=PWM_FREQ)
pwm_b = PWM(Pin(BLUE_PIN), freq=PWM_FREQ)


def value_map(value, in_min, in_max, out_min, out_max):
    """
    This is a function we wrote ourselves, because MicroPython has no map() function the way Arduino does.
    It takes a number from one range and rescales it into another range, which is how we turn a light level into a
    brightness.
    """
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def write_colour(pwm, brightness):
    """
    This function sends one colour channel to its pin.
    We think about colours as numbers from 0 to 255, the way almost every program does, but duty_u16() wants a number
    from 0 to 65535. This function does that conversion in one place, so the colour code below stays easy to read.
    """
    pwm.duty_u16(int(brightness * 65535 / 255))


# Print out the initial message so we know that the program started successfully.
print("RGB LED Controller with full-spectrum color mapping started")

while True:

    """
    read() reads the voltage at the analog pin and converts it into a number. Since the NULA board uses a 12-bit ADC,
    the value runs from 0 in complete darkness to 4095 in bright light. The more light falls on the photoresistor, the
    lower its resistance and the higher this number becomes.
    """
    ldr_value = ldr.read()
    print("LDR value:", ldr_value)

    """
    This is where the colour is decided. We split the light range into three parts and give each one its own transition,
    so that the colour never jumps: it always slides from wherever it was into the next colour.
    Notice how in each part one channel is being mapped upwards while another is mapped downwards, which is exactly what
    makes one colour fade into the next.
    """
    if ldr_value <= FIRST_THIRD:

        # Darkest third: fade from red (255, 0, 0) to green (0, 255, 0).
        r = value_map(ldr_value, 0, FIRST_THIRD, 255, 0)
        g = value_map(ldr_value, 0, FIRST_THIRD, 0, 255)
        b = 0

    elif ldr_value <= SECOND_THIRD:

        # Middle third: fade from green (0, 255, 0) to blue (0, 0, 255).
        r = 0
        g = value_map(ldr_value, FIRST_THIRD + 1, SECOND_THIRD, 255, 0)
        b = value_map(ldr_value, FIRST_THIRD + 1, SECOND_THIRD, 0, 255)

    else:

        """
        Brightest third: fade from blue (0, 0, 255) to white (255, 255, 255). White is simply all three channels on at
        once, which is why red and green rise here while blue stays at full brightness.
        """
        r = value_map(ldr_value, SECOND_THIRD + 1, 4095, 0, 255)
        g = value_map(ldr_value, SECOND_THIRD + 1, 4095, 0, 255)
        b = 255

    """
    Here we write all three channels at once, which is what mixes the colour.
    """
    write_colour(pwm_r, r)
    write_colour(pwm_g, g)
    write_colour(pwm_b, b)

    # Print the mixed colour too, so we can compare it against the light level above.
    print("RGB:", r, g, b)

    # A short pause between readings. Keeping it small makes the colour changes look smooth.
    time.sleep_ms(100)
