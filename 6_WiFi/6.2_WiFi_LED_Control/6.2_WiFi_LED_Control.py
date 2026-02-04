"""
@file     6.2_WiFi_LED_Control.py
@brief		Example that builds a web server through ESP32 to control
          its outputs for toggling the LED ON/OFF.

@author		Soldered
"""

# Import socket library for creating the web server using Python socket API
import socket
# Import network library that allows connection to WiFi network
import network
# Import Pin module for LED
from machine import Pin

# WiFi network credentials
ssid = ''
password = ''

# Create a WLAN network object and set the ESP as a WiFi station to connect to WiFi access points
station = network.WLAN(network.STA_IF)

# Activate the station and connect to the network
station.active(True)
station.connect(ssid, password)

# Ensure the ESP is connected before proceeding
while station.isconnected() == False:
    pass

# After successful connection, get and print IP network interface parameters
# Printed parameters are: IP address, subnet mask, gateway and DNS server
print('Connection successful')
print(station.ifconfig())

# Create Pin object for LED on GPIO 5
led = Pin(5, Pin.OUT)

# Function that generates the HTML web page to control and display the LED state
def web_page():
  # Check LED state
  if led.value() == 1:
    gpio_state="ON"
  else:
    gpio_state="OFF"
  
  # Basic HTML code, generates document with buttons to control LED state
  html = """
    <html>
        <head>
            <title>Web Server LED Control</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="icon" href="data:,">
            <style>
                html { display:inline-block; margin: 0px auto; text-align: center; }
                h1 { color: #0F3376; padding: 2vh; }
                p { font-size: 1.5rem; }
                .button { background-color: green; border: none; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; }
                .button2 { background-color: red; }
            </style>
        </head>
        <body>
            <h1>LED Web Server</h1>
            <p>LED state: <strong>""" + gpio_state + """</strong></p>
            <p><a href="/?led=on"><button class="button">ON</button></a></p>
            <p><a href="/?led=off"><button class="button button2">OFF</button></a></p></body>
    </html>"""
  # Return 'html' string to display web content
  return html                                                       

# Create a new socket
s = socket.socket()

# Method to allow socket to bind to a port if it was recently used to avoid 'already in use' error when restarting
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to an address (network interface and port number)
s.bind(('', 80))

# Enable the server to accept connections by specifying maximum number of queued connections
s.listen(2)

try:
    # Infinite loop
    while True:
        # Wait for a client (browser) to connect, save new socket object 'conn' to send and receive data
        # on connection, 'addr' is the ip address of the client
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        
        # Receive data from the socket by reading up to 1024 bytes of HTTP request
        request = conn.recv(1024)
        # Convert it to string
        request = str(request)
        
        # Search inside the request for '/?led=on' or '/?led=off'
        led_on = request.find('/?led=on')
        led_off = request.find('/?led=off')
        # If the string is found at position 6 in the request -> toggle LED
        if led_on == 6:
            print('LED ON')
            led.value(1)
        if led_off == 6:
            print('LED OFF')
            led.value(0)
            
        # Call the function to generate and send the HTML page along with HTTP headers
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        
        # Close the created socket (IMPORTANT)
        conn.close()
        
# Press CTRL + C (or Thonny Stop) to close the listening socket (Shutdown the server)
except KeyboardInterrupt:
    print("Server stopped")
    s.close()
