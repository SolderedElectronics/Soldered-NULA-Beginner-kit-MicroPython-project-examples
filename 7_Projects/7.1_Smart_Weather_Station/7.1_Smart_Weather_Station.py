"""
@file       7.1_Smart_Weather_Station.py
@brief      Project that brings together three things you have already learned separately: the SHTC3 temperature
            and humidity sensor from section 5, the LCD display from section 4, and the Wi-Fi connection from
            section 6. The board measures temperature and humidity, shows them on the LCD, and sends them to a
            webhook on the internet so you can follow the readings from anywhere.
            For details, connection diagram and more, check out the example documentation at: <link placeholder>

@author     Soldered Electronics
"""

# I2C is what the Qwiic connector carries, and both the sensor and the display are Qwiic modules.
from machine import I2C, Pin

# The Soldered drivers for the SHTC3 sensor and the LCD display, both found in the lib folder of this repository.
from SHTC3 import SHTC3
from LCD import LCD_I2C

# The network module joins a Wi-Fi network, and urequests lets us speak HTTP.
import network
import urequests
import time

"""
These two variables hold the name of your Wi-Fi network (the SSID) and its password. Replace the text between the
quotation marks with your own network details.
"""
ssid = "your ssid"
password = "your password"

"""
This variable holds the address we send our readings to. Open https://webhook.site in a browser, copy the unique link
it shows you, and paste it between the quotation marks below. Keep that browser tab open and you will see every
reading appear in it.
"""
webhook_url = "your unique url"

"""
Here we set up the I2C connection. On the NULA MINI, I2C uses IO6 for the data line (SDA) and IO7 for the clock line
(SCL), which are the pins the Qwiic connector is wired to. Notice that both modules share this one connection: that is
what lets you chain several Qwiic modules together without defining any pins for them.
"""
i2c = I2C(0, scl=Pin(7), sda=Pin(6))

"""
Here we create our two objects, one for the sensor and one for the display, and hand both of them the same I2C
connection. An object is our way of talking to a device: every function we call on it, we call through its name.
"""
shtc3 = SHTC3(i2c)
lcd = LCD_I2C(i2c)

"""
These two variables hold the latest readings, and the two below them control how much time passes between readings.
30000 milliseconds is thirty seconds. Feel free to experiment with that value, but keep in mind that every reading is
also sent over the internet.
"""
temperature = 0.0
humidity = 0.0
last_update = 0
UPDATE_MS = 30000

"""
Here we prepare the display. begin() starts the communication and has to come first. backlight() then turns on the
light behind the screen, and it has to come after begin(), which would otherwise switch it back off. clear() wipes
anything left on the screen from before.
setCursor() chooses where the next text appears: the first number is the column and the second is the row, and both
start counting at zero. We show a short greeting first, so we can tell at a glance that the display itself works.
"""
lcd.begin()
lcd.backlight()
lcd.clear()
lcd.setCursor(0, 0)
lcd.print("Weather Station")
lcd.setCursor(0, 1)
lcd.print("Starting...")
time.sleep(1)
lcd.clear()

"""
begin() on the sensor prepares it for use and tells us whether it answered, giving back True on success and False on
failure. The "not" in front means the opposite, so this reads as "if the sensor did not start".
If the sensor is missing there is nothing left for this project to measure, so instead of continuing we print the
problem and stop here. The while True loop below never ends, which is a simple way of saying "go no further".
"""
if not shtc3.begin():
    print("SHTC3 init failed!")
    lcd.print("SHTC3 error!")
    while True:
        time.sleep(0.1)

"""
Here we create our network object and switch the Wi-Fi hardware on, then start the connection attempt. connect() does
not wait for the connection to finish, so we tell the user what is going on both in the console and on the display.
"""
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
print("Connecting to Wi-Fi", end="")
lcd.setCursor(0, 0)
lcd.print("Connecting WiFi")
wlan.connect(ssid, password)

"""
Here we wait for the connection ourselves. isconnected() tells us whether we are online yet.
"""
while not wlan.isconnected():
    time.sleep(0.5)
    print(".", end="")
    lcd.setCursor(0, 1)
    lcd.print(".")

# ifconfig() returns the address the router handed out to our board as its first value.
print()
print("Wi-Fi connected!")
print("IP:", wlan.ifconfig()[0])

# Let the user know we are online, then clear the display so the readings start on an empty screen.
lcd.clear()
lcd.print("WiFi Connected!")
time.sleep(0.8)
lcd.clear()

print("Smart Weather Station ready!")

while True:

    """
    time.ticks_ms() is a function that returns the number of milliseconds passed since the board was powered on. We use
    it instead of a plain sleep so the board stays free to do other work between readings.
    """
    now = time.ticks_ms()

    """
    Here we check how much time has passed since the last reading. Only when UPDATE_MS milliseconds have gone by do we
    take a new one, and we immediately remember the current time as the new starting point.
    """
    if time.ticks_diff(now, last_update) >= UPDATE_MS:
        last_update = now

        """
        sample() tells the sensor to perform a fresh measurement, and the two read functions then hand us the results.
        We have to call sample() first, otherwise we would keep getting the previous measurement.
        """
        shtc3.sample()
        temperature = shtc3.readTemperature()
        humidity = shtc3.readHumidity()

        # Print the readings to the console. ":.2f" tells Python to show a number with two decimal places.
        print("Temperature: {:.2f} °C, Humidity: {:.2f} %".format(temperature, humidity))

        """
        Now we show the same readings on the display. We clear it first, because writing shorter text over longer text
        would leave leftover characters behind.
        "\xDF" is the character code the display uses for the degree symbol. The console and the LCD do not use the
        same character set, which is why we write the degree sign one way above and another way here.
        """
        lcd.clear()
        lcd.setCursor(0, 0)
        lcd.print("Temp: {:.1f}\xDFC".format(temperature))
        lcd.setCursor(0, 1)
        lcd.print("Hum: {:.1f} %".format(humidity))

        """
        Before sending anything we check that we are still online. A Wi-Fi connection can drop at any time, and trying
        to send data without one would only waste time and print errors.
        """
        if wlan.isconnected():

            """
            Here we build the data we are going to send. The format "name=value&name=value" is the same one a browser
            uses when you submit a simple web form: the ampersand ("&") separates one value from the next.
            """
            post_data = "temperature={:.2f}&humidity={:.2f}".format(temperature, humidity)

            """
            We wrap the request in a try block because anything that goes over a network can fail, and without it a
            failed request would stop the whole program with an error.
            """
            try:

                """
                post() sends the request together with our data and waits for the answer. The header we pass along
                describes the format our data is written in, so the server knows how to read it.
                """
                response = urequests.post(
                    webhook_url,
                    data=post_data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )

                print("POST successful! Response code:", response.status_code)

                # close() releases the memory the response was using. Always close a response once you are done.
                response.close()

            except Exception as e:
                print("POST failed. Error:", e)

        else:

            # If we lost the connection, start a new attempt and try again on the next reading.
            print("Wi-Fi disconnected. Trying to reconnect...")
            wlan.connect(ssid, password)

    # A very short pause leaves the processor a moment to handle its own background work.
    time.sleep_ms(10)
