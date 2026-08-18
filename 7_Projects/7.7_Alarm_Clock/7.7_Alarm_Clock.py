"""
@file       7.7_Alarm_Clock.py
@brief      Project that builds a Wi-Fi connected alarm clock. The board joins your network, asks an NTP server on
            the internet what the time is, and shows the current time on the LCD display. Two buttons set the alarm
            hour and minute, and when the alarm time is reached the buzzer sounds a series of beeps.
            It brings together the LCD from section 4, the button debouncing from section 2.2, the buzzer from
            section 2.4 and the Wi-Fi connection from section 6.
            For details, connection diagram and more, check out the example documentation at: <link placeholder>

@author     Soldered
"""

# I2C is what the Qwiic connector carries, PWM drives the buzzer, and Pin reads the two buttons.
from machine import I2C, Pin, PWM

# The Soldered driver for the LCD display, found in the lib folder of this repository.
from LCD import LCD_I2C

# The network module joins a Wi-Fi network.
import network

"""
The ntptime module asks an NTP server on the internet what the time is and sets the clock of the board from the answer.
NTP stands for Network Time Protocol, and it is how nearly every device on the internet keeps its clock correct.
"""
import ntptime
import time

"""
These two variables hold the name of your Wi-Fi network (the SSID) and its password. Replace the text between the
quotation marks with your own network details.
"""
WIFI_SSID = "your ssid"
WIFI_PASS = "your password"

"""
NTP servers always answer in UTC, the world reference time, so we have to tell the board how far our own time zone sits
from it. The offset is given in seconds, so one hour is 3600. Croatia in winter is one hour ahead of UTC, which would be
3600 here.
The second value is the extra offset for daylight saving time. Set it to 3600 during summer time in a country that uses
it, and leave it at 0 otherwise.
"""
GMT_OFFSET_SEC = 0
DAYLIGHT_OFFSET_SEC = 0

"""
These are the variables to which we pass the numbers of pins that we had connected the two BUTTONS and the buzzer to.
One button counts the alarm hour up, the other counts the alarm minute up.
The NULA board has a pin naming logic as follows: IO2, where 2 is the number that we give to the variable.
If you wish to use a different pin, make sure you are using a IO__ marked pin.
"""
BUTTON_HOUR = 2
BUTTON_MIN = 3
BUZZER_PIN = 4

"""
These variables hold the alarm time we are counting towards, starting at 07:00, and remember whether the alarm has
already gone off, so that it sounds once and not over and over during the same minute.
"""
alarm_hour = 7
alarm_minute = 0
alarm_triggered = False

"""
This variable remembers which minute the alarm last went off in. Without it, stopping the alarm with a button press
inside the very minute it fired would let it fire again immediately, over and over until the minute was out. We start it
at -1, a value no real minute can have, so that the first alarm is never blocked.
"""
last_alarm_minute = -1

"""
This variable remembers whether we ever managed to reach the time server. Until we have, the clock of the board is not
set to anything meaningful, so we must not compare the alarm against it.
"""
time_synced = False

"""
These are the variables used for button debouncing, the same technique explained in example 2.2. Because we have two
buttons here, each one needs its own pair of variables: one remembering its previous state and one remembering when
that state last changed.
"""
last_hour_state = 1
last_min_state = 1
last_hour_change_ms = 0
last_min_change_ms = 0
DEBOUNCE_MS = 25

"""
These two variables control how often we ask the NTP server for the time again. A board's own clock drifts slowly, so
checking in every once in a while keeps it accurate.
"""
last_sync = 0
SYNC_INTERVAL_MS = 60000

"""
Here we set up the I2C connection and create our display object. On the NULA MINI, I2C uses IO6 for the data line (SDA)
and IO7 for the clock line (SCL), which are the pins the Qwiic connector is wired to.
"""
i2c = I2C(0, scl=Pin(7), sda=Pin(6))
lcd = LCD_I2C(i2c)

"""
Here we create our Pin objects for the two buttons. Pin.IN tells the board that these pins should read a value, and
Pin.PULL_UP switches on a resistor inside the chip that ties each pin to 3.3V while its button is released. That means a
pin reads high (1) when its button is up and low (0) while it is pressed.
"""
hour_btn = Pin(BUTTON_HOUR, Pin.IN, Pin.PULL_UP)
min_btn = Pin(BUTTON_MIN, Pin.IN, Pin.PULL_UP)

"""
Here we create our PWM object for the buzzer. duty_u16() sets what fraction of the time the pin stays on, as a number
from 0 (always off) to 65535 (always on). Half of that gives a buzzer its clearest tone.
"""
buzzer = PWM(Pin(BUZZER_PIN))
SOUND_ON = 32768
SOUND_OFF = 0
buzzer.duty_u16(SOUND_OFF)


def get_current_time():
    """
    This is a function we wrote ourselves. It returns the current hour and minute in our own time zone.
    time.time() gives us the time the board knows, counted in seconds, and adding our two offsets to it moves that from
    UTC into local time. time.localtime() then splits the result into separate pieces, of which position 3 is the hour
    and position 4 is the minute.
    """
    local = time.localtime(time.time() + GMT_OFFSET_SEC + DAYLIGHT_OFFSET_SEC)
    return local[3], local[4]


def sync_time():
    """
    This function asks the NTP server for the time and sets the clock of the board from the answer.
    We wrap it in a try block because anything that goes over a network can fail, and a failed sync should not stop the
    whole clock.
    """
    try:
        ntptime.settime()
        return True
    except Exception as e:
        print("Failed to obtain time from NTP:", e)
        return False


def beep_alarm():
    """
    This function sounds the alarm. freq() sets the pitch, 1000 Hz in this case, and switching the sound on and off five
    times in a row is what turns one long tone into a series of beeps.
    Feel free to experiment with the frequency, the number of repeats and the two pauses.
    """
    buzzer.freq(1000)
    for _ in range(5):
        buzzer.duty_u16(SOUND_ON)
        time.sleep_ms(300)
        buzzer.duty_u16(SOUND_OFF)
        time.sleep_ms(100)


"""
Here we prepare the display. begin() starts the communication and has to come first. backlight() then turns on the light
behind the screen, and it has to come after begin(), which would otherwise switch it back off.
"""
lcd.begin()
lcd.backlight()

"""
clear() wipes anything left on the screen from before, and setCursor() chooses where the next text appears: the first
number is the column and the second is the row, both counting from zero.
"""
lcd.clear()
lcd.setCursor(0, 0)
lcd.print("Connecting WiFi")

"""
Here we create our network object, switch the Wi-Fi hardware on and start the connection attempt. connect() does not
wait for the connection to finish, so we wait for it ourselves in the loop below. isconnected() tells us whether we are
online yet.
"""
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASS)
while not wlan.isconnected():
    time.sleep(0.5)
    print(".", end="")

print()
print("WiFi connected!")
lcd.clear()
lcd.print("WiFi connected")
time.sleep(1)

"""
Now that we are online we can ask for the time. Unlike Arduino, MicroPython waits for the answer here, so once this
returns successfully the clock is already correct.
"""
if sync_time():
    time_synced = True
    last_sync = time.ticks_ms()
    lcd.clear()
    lcd.print("Time synced!")
else:
    lcd.clear()
    lcd.print("Sync failed!")
time.sleep(1)
lcd.clear()

while True:

    """
    If we never reached the time server, the clock of the board is not set to anything meaningful. Showing it would be
    misleading and comparing the alarm against it could set the alarm off at the wrong moment, so we say what is going
    on and try the sync again on the next pass.
    continue jumps straight back to the top of the loop.
    """
    if not time_synced:
        lcd.setCursor(0, 0)
        lcd.print("Waiting for time")
        if time.ticks_diff(time.ticks_ms(), last_sync) > SYNC_INTERVAL_MS:
            if sync_time():
                time_synced = True
                lcd.clear()
            last_sync = time.ticks_ms()
        time.sleep_ms(100)
        continue

    # Here we read the current time through our own function above.
    hour, minute = get_current_time()

    """
    Here we build the text for the display. "{:02d}" means "a whole number written with at least two digits, padded with
    a zero if needed", which is what turns 7 minutes past into "07" instead of "7".
    """
    lcd.setCursor(0, 0)
    lcd.print("Time: {:02d}:{:02d}".format(hour, minute))

    # On the second line we show the alarm time, padded the same way.
    lcd.setCursor(0, 1)
    lcd.print("Alarm {:02d}:{:02d}".format(alarm_hour, alarm_minute))

    """
    This is the debouncing logic for the hour button, the same one explained in example 2.2. value() reads the pin,
    time.ticks_ms() returns the number of milliseconds passed since the board was powered on, and together they let us
    ignore any change that comes too soon after the previous one to be a real press.
    Because the buttons read high when released, a press is the moment the reading goes from 1 to 0, and that is exactly
    the moment we count the hour up. After 23 we start over at 0, since there is no hour 24.
    """
    hour_reading = hour_btn.value()
    now = time.ticks_ms()
    if hour_reading != last_hour_state and time.ticks_diff(now, last_hour_change_ms) > DEBOUNCE_MS:
        last_hour_change_ms = now
        if last_hour_state == 1 and hour_reading == 0:
            alarm_hour = (alarm_hour + 1) % 24
        last_hour_state = hour_reading

    # The very same logic for the minute button, counting up to 59 before starting over.
    min_reading = min_btn.value()
    if min_reading != last_min_state and time.ticks_diff(now, last_min_change_ms) > DEBOUNCE_MS:
        last_min_change_ms = now
        if last_min_state == 1 and min_reading == 0:
            alarm_minute = (alarm_minute + 1) % 60
        last_min_state = min_reading

    """
    Here we check whether it is time for the alarm. All three conditions have to be true at once: the hour has to match,
    the minute has to match, and the alarm must not have gone off already. That last check is what the alarm_triggered
    variable is for, since without it the alarm would sound again and again for the whole minute.
    """
    if hour == alarm_hour and minute == alarm_minute and not alarm_triggered and minute != last_alarm_minute:
        alarm_triggered = True
        last_alarm_minute = minute
        lcd.clear()
        lcd.setCursor(0, 0)
        lcd.print("ALARM!")
        print("Alarm Triggered!")
        beep_alarm()

    """
    Pressing either button after the alarm has gone off clears the warning from the display and arms the alarm again for
    the next day.
    """
    if alarm_triggered and (hour_reading == 0 or min_reading == 0):
        alarm_triggered = False
        lcd.clear()

    # And here we ask the NTP server for the time again every so often, so that the clock does not drift.
    if time.ticks_diff(time.ticks_ms(), last_sync) > SYNC_INTERVAL_MS:
        sync_time()
        last_sync = time.ticks_ms()

    """
    A short pause so the display is not rewritten thousands of times per second. Keeping it short also keeps the buttons
    feeling responsive.
    """
    time.sleep_ms(100)
