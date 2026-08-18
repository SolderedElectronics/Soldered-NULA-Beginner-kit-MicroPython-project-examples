"""
@file       7.3_Parking_sensor.py
@brief      Project that builds the parking sensor you know from cars. The Soldered Ultrasonic Distance Sensor
            watches for obstacles, and the closer one gets, the faster the buzzer beeps. Under 10 cm the beeping
            turns into one continuous tone and an LED lights up as a final warning.
            It builds on the distance measuring from section 3.1 and the buzzer from section 2.4.
            For details, connection diagram and more, check out the example documentation at: <link placeholder>

@author     Soldered
"""

# The Soldered driver for the Ultrasonic Distance Sensor, found in the lib folder of this repository.
from UltrasonicSensor import UltrasonicSensor

# I2C is what the Qwiic connector carries, PWM drives the buzzer, and a plain Pin is enough for the warning LED.
from machine import I2C, Pin, PWM
import time

"""
This is a variable to which we pass the number of pin that we had connected the buzzer to.
The NULA board has a pin naming logic as follows: IO2, where 2 is the number that we give to the variable.
If you wish to use a different pin, make sure you are using a IO__ marked pin.
"""
BUZZER_PIN = 2

"""
This is a variable to which we pass the number of pin that we had connected the warning LED to.

Remember that the LED needs a 330 Ohm resistor in series with it. That resistor limits how much current flows, and
without it the LED draws more than either it or the pin is built for, so both can be damaged.
"""
LED_PIN = 5

"""
This is the frequency of the warning sound, in Hertz. A frequency is how many times per second the buzzer moves back
and forth, and our ears hear it as the pitch of the sound. Small buzzers like this one are loudest somewhere between
2 and 4 kHz, so feel free to experiment with this value until it sounds best to you.
"""
TONE_FREQ = 2700

"""
This is how long we wait after asking for a measurement, in milliseconds. The sensor gives up listening for an echo
after 38 milliseconds, so waiting a little longer than that means the answer is always ready when we ask for it.
This wait also sets the pace of the whole loop, which is why there is no pause at the bottom of it.
"""
MEASURE_WAIT_MS = 50

"""
Here we set up the I2C connection. The two pins are fixed by the board: on the NULA MINI, I2C uses IO6 for the data
line (SDA) and IO7 for the clock line (SCL), which are exactly the pins the Qwiic connector is wired to.
"""
i2c = I2C(0, scl=Pin(7), sda=Pin(6))

"""
Here we create our sensor object, which we named "sensor", and hand it the I2C connection. We pass no pin numbers for
the sensor itself: every Qwiic module shares those same two I2C pins, and this sensor answers on address 0x30.
"""
sensor = UltrasonicSensor(i2c)

"""
Here we create our PWM object for the buzzer and set its pitch once, since it never changes in this project.
duty_u16() sets what fraction of the time the pin stays on, as a number from 0 (always off) to 65535 (always on). Half
of that is the even on-off switching that gives a buzzer its clearest tone.
"""
buzzer = PWM(Pin(BUZZER_PIN))
buzzer.freq(TONE_FREQ)
SOUND_ON = 32768
SOUND_OFF = 0
buzzer.duty_u16(SOUND_OFF)

"""
Here we create our Pin object for the LED. Pin.OUT tells the board that this pin should write a value instead of
reading one. Right after that we write 0 to it, so the warning light starts out switched off.
"""
led = Pin(LED_PIN, Pin.OUT)
led.value(0)

"""
These three variables are what lets us beep at different speeds without ever stopping the program.
"last_beep" remembers the moment the buzzer was last switched on or off, "beep_interval" holds how long we want to
wait between those switches, and "buzzer_on" remembers whether the buzzer is currently sounding or silent.
"""
last_beep = 0
beep_interval = 0
buzzer_on = False

# begin() prepares the sensor for use, before we start reading from it.
sensor.begin()

# Print out the initial message so we know that the program started successfully.
print("Ultrasonic buzzer + LED reverse sensor started")

while True:

    """
    Reading a Qwiic sensor takes two steps. takeMeasure() asks the sensor to send out a pulse and time the echo, and
    the wait afterwards gives it the moment it needs to finish that work and store the answer.
    """
    sensor.takeMeasure()
    time.sleep_ms(MEASURE_WAIT_MS)

    """
    getDistance() then fetches the stored answer, already converted into centimeters. The value comes back as a whole
    number of centimeters, which is all the accuracy this sensor can honestly offer.
    """
    distance = sensor.getDistance()

    """
    The sensor answers with 0 when it heard no echo at all, which happens when nothing is in range or when the surface
    in front of it scatters the sound away. That is not a real measurement, and treating it as one would set off the
    alarm at full blast whenever the way is clear, so instead we fall silent and wait for the next measurement.
    continue jumps straight back to the top of the loop.
    """
    if distance == 0:
        print("No echo received, nothing in range.")
        buzzer.duty_u16(SOUND_OFF)
        buzzer_on = False
        led.value(0)
        continue

    # Print the measured distance to the console so we can follow along while testing.
    print("Distance from obstacle: {} cm".format(distance))

    """
    We switch the LED off at the start of every pass through the loop. Only the closest range switches it back on again
    a few lines below, so this one line saves us from having to turn it off in every other case.
    """
    led.value(0)

    """
    This chain of if statements is the heart of the project: it turns a distance into a beeping speed. Each range gets a
    different value of beep_interval, and a smaller interval means less waiting between beeps, which we hear as faster
    beeping. The board checks the ranges from the widest down and stops at the first one that matches.
    Feel free to experiment with both the distances and the intervals.
    """
    if distance > 100:

        # Nothing in range. An interval of 0 keeps the buzzer silent, and here we make sure it really is silent.
        beep_interval = 0
        buzzer.duty_u16(SOUND_OFF)
        buzzer_on = False

    elif distance > 60:

        # Between 60 and 100 cm, beep slowly.
        beep_interval = 800

    elif distance > 30:

        # Between 30 and 60 cm, beep at a medium speed.
        beep_interval = 400

    elif distance > 10:

        # Between 10 and 30 cm, beep quickly.
        beep_interval = 150

    else:

        """
        Closer than 10 cm. Here we leave the sound switched on instead of beeping, which makes one continuous tone, and
        we light up the LED as a final warning.
        """
        buzzer.duty_u16(SOUND_ON)
        buzzer_on = True
        beep_interval = 0
        led.value(1)

    """
    This is where the beeping itself happens. time.ticks_ms() is a function that returns the number of milliseconds
    passed since the board was powered on. By comparing it against the moment of the last switch we can wait the right
    amount of time without pausing the program, which would stop us from measuring.
    Every time the interval has passed we flip buzzer_on to its opposite value with the "not" operator, and then either
    start the sound or stop it. Doing that over and over is what produces a beep.
    """
    if beep_interval > 0:
        now = time.ticks_ms()
        if time.ticks_diff(now, last_beep) >= beep_interval:
            last_beep = now
            buzzer_on = not buzzer_on
            if buzzer_on:
                buzzer.duty_u16(SOUND_ON)
            else:
                buzzer.duty_u16(SOUND_OFF)
