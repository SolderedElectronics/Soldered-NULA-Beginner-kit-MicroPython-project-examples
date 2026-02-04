"""
@file       6.1_Connection_And_Getting_Data.py
@brief	    Example that connects to a WiFi network and retrieves data from a web server with a GET request.

@author		Soldered
"""

# Import network library that allows connection to WiFi network
import network
# Import module for making HTTP requests
import urequests

ssid = ""
password = ""

# Webhook.site generates free, unique URLs that lets you see everything that's sent there instantly (POST, GET requests)
request_url = "https://webhook.site/YOUR_UNIQUE_ID"

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

# Make a GET request to the specified URL and store the servers response
print(f"Making GET request to: {request_url}")
response = urequests.get(request_url)

# Print the response status code and body 
print("Response status:", response.status_code)
print("Response body:\n", response.text)
