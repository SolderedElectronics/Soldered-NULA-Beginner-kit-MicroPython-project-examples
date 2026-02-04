"""
@file		7.4_Alarm_Clock.py
@brief		An alarm clock using an LCD display, buttons to set the alarm time,
            and a buzzer to sound the alarm. The clock synchronizes time from NTP server.

@author		Soldered
"""

from machine import Pin, PWM, I2C
from LCD import LCD_I2C
import time
import ntptime
import network

i2c = I2C(0, scl=Pin(7), sda=Pin(6))
lcd = LCD_I2C(i2c)

# Initialize sensor over Qwiic
# lcd = LCD_I2C()

lcd.backlight()
lcd.begin()

ssid = ""
password = ""

synced_at = 0

HOUR_BTN_PIN = 4
MINUTES_BTN_PIN = 5
BUZZER_PIN = 19
BUZZER_FREQ = 2000
ALARM_MAX_SEC = 60

hour_btn = Pin(HOUR_BTN_PIN, Pin.IN, Pin.PULL_UP)
minutes_btn = Pin(MINUTES_BTN_PIN, Pin.IN, Pin.PULL_UP)

hour_btn_last = 1
minutes_btn_last = 1
hour_btn_last_time = 0
minutes_btn_last_time = 0
DEBOUNCE_MS = 200

buzzer = PWM(Pin(BUZZER_PIN))
buzzer.freq(BUZZER_FREQ)
buzzer.duty(0)

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        lcd.setCursor(0, 0)
        lcd.print("Connecting....")
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    lcd.clear()
    lcd.print("WiFi Connected")

def sync_time():
    try:
        ntptime.settime()
        global synced_at
        synced_at = time.ticks_ms()
    except Exception as e:
        print("Failed to synchronize time:", e)

def print_alarm_time(hour, minute):
    lcd.clear()
    lcd.setCursor(1, 0)
    lcd.print("Alarm set for:")
    lcd.setCursor(5, 1)
    lcd.print("{:02}:{:02}".format(hour, minute))

def play_alarm():
    for _ in range(3):
        buzzer.duty(512)
        time.sleep(0.1)
        buzzer.duty(0)
        time.sleep(0.1)

connect_wifi(ssid, password)
time.sleep(2)
sync_time()

alarm_hour = 0
alarm_minute = 0
alarm_set = False
reset_alarm = False

print_alarm_time(alarm_hour, alarm_minute)

while True:
    # Sync time every minute
    if time.ticks_diff(time.ticks_ms(), synced_at) >= 60000:
        sync_time()

    if reset_alarm:
        alarm_hour = 0
        alarm_minute = 0
        reset_alarm = False

    current_time = time.localtime(time.time() + 3600)
    hour = current_time[3]
    minute = current_time[4]

    # Check for hour button press
    if hour_btn.value() == 0 and hour_btn_last == 1:
        if time.ticks_diff(time.ticks_ms(), hour_btn_last_time) > DEBOUNCE_MS:
            alarm_hour = (alarm_hour + 1) % 24
            print_alarm_time(alarm_hour, alarm_minute)
            hour_btn_last_time = time.ticks_ms()
    hour_btn_last = hour_btn.value()

    # Check for minutes button press
    if minutes_btn.value() == 0 and minutes_btn_last == 1:
        if time.ticks_diff(time.ticks_ms(), minutes_btn_last_time) > DEBOUNCE_MS:
            alarm_minute = (alarm_minute + 1) % 60
            print_alarm_time(alarm_hour, alarm_minute)
            minutes_btn_last_time = time.ticks_ms()
    minutes_btn_last = minutes_btn.value()
    
    # Check for alarm
    if hour == alarm_hour and minute == alarm_minute:
        lcd.clear()
        lcd.print("ALARM!")
        alarm_running = True
        alarm_start_time = time.ticks_ms()
        while True:
            # Play alarm sound every 2 seconds
            if time.ticks_diff(time.ticks_ms(), alarm_start_time) % 2000 < 100:
                play_alarm()
            if hour_btn.value() == 0 or minutes_btn.value() == 0:
                lcd.clear()
                lcd.print("Alarm stopped.")
                buzzer.duty(0)
                break
            if time.ticks_diff(time.ticks_ms(), alarm_start_time) >= ALARM_MAX_SEC * 1000:
                lcd.clear()
                lcd.print("Alarm expired!")
                buzzer.duty(0)
                break
        reset_alarm = True
        time.sleep(1)  # Small delay after alarm
        
    # Small delay to avoid busy loop   
    time.sleep(0.1)
