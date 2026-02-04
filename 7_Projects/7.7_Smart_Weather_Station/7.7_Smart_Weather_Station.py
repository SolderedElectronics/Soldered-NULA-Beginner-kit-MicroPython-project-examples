"""
@file		7.7_Smart_Weather_Station.py
@brief		Example demonstrating how to create a smart weather station using
            the SHTC3 temperature and humidity sensor along with an I2C LCD display. 
            After reading, data is sent to a web server via POST request.

@author		Soldered
"""

from machine import Pin, I2C
from LCD import LCD_I2C
from SHTC3 import SHTC3
import network
import urequests
import time

# Initialize I2C for LCD and SHTC3
i2c = I2C(0, scl=Pin(7), sda=Pin(6))
lcd = LCD_I2C(i2c)
shtc3 = SHTC3(i2c)
lcd = LCD_I2C(i2c)

lcd.backlight()
lcd.begin()

ssid = ""
password = ""

wlan = network.WLAN(network.STA_IF)

wlan.active(True)
wlan.connect(ssid, password)

while wlan.isconnected() == False:
    pass

lcd.print("WiFi Connected")

time.sleep(2)
lcd.clear()

WEBHOOK_URL = "https://webhook.site/YOUR-UNIQUE-ID"

last_send_time = 0

while True:
    shtc3.sample()

    temperature = shtc3.readTemperature()
    humidity = shtc3.readHumidity()

    lcd.setCursor(0, 0)
    lcd.print("Temp: {:.1f} C".format(temperature))
    lcd.setCursor(0, 1)
    lcd.print("Humidity: {:.2f}%".format(humidity))

    time.sleep(2)
    lcd.clear()

    if time.ticks_diff(time.ticks_ms(), last_send_time) >= 10000:
        data = {
            "temperature": temperature,
            "humidity": humidity
        }
        try:
            response = urequests.post(WEBHOOK_URL, json=data)
            response.close()
            lcd.print("Data sent!")
            time.sleep(1)
            lcd.clear()
        except Exception as e:
            print("Failed to send data:", e)

        last_send_time = time.ticks_ms()