"""
@file		6.3_Sending_Data.py
@brief		Example that sends data via POST request to Webhook service.

@author		Soldered
"""

# Import network library that allows connection to WiFi network
import network
# Import module for making HTTP requests
import urequests
import time
import random

# WiFi network credentials used to connect to an existing WiFi network
ssid = ""
password = ""

# Webhook.site generates free, unique URLs that lets you see everything that's sent there instantly (POST, GET requests)
WEBHOOK_URL = "https://webhook.site/YOUR_UNIQUE_ID"

# Create a WLAN network object and set the ESP as a WiFi station to connect to WiFi access points
wlan = network.WLAN(network.STA_IF)

# Activate network interface and connect to the specified wireless network using SSID and PASSWORD
wlan.active(True)
wlan.connect(ssid, password)

# Ensure the ESP is connected to WiFi network before proceeding
while wlan.isconnected() == False:
  pass

# Print IP parameters: IP address, subnet mask, gateway and DNS server
print('Connection successful')
print(f"IP config: {wlan.ifconfig()}")

# Initialize timer variable to send data every 10 seconds (this approach sends data immediately)
last_send_time = time.ticks_ms() - 10000

# Main loop
while True:
    # If ten seconds has passed, send data via POST request
    if time.ticks_diff(time.ticks_ms(), last_send_time) > 10000:
        # Store data to send in dictionary format: random value and timestamp
        random_value = random.randint(0, 100)
        data = {
            "value" : random_value,
            "timestamp" : time.ticks_ms()
            }
        try:
            # Send a POST request to the specified URL with data in JSON format
            response = urequests.post(WEBHOOK_URL, json=data)
            
            # Print HTTP status code returned by the server
            print("POST status: ", response.status_code)
            # Print the response body returned by the server
            print("POST body: ", response.text)
            # Close the response to free up memory
            response.close()
            
        # Catch any exception (network issue, timeout, ...) and print it out
        except Exception as e:
            print("POST failed: ", e)
            
        # Update the timestamp of last time data was sent
        last_send_time = time.ticks_ms()
    
    # Add small delay to program
    time.sleep_ms(10)
