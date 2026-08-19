"""
@file       6.2_Wi-Fi_LED_Control.py
@brief      Example that shows how to control an LED from a web page. The NULA board joins your Wi-Fi network and
            then becomes a small web server of its own, which means you can open it in the browser of your phone
            or computer. The page has an ON and an OFF button and shows the current state of the LED.
            In the previous example the board asked a website for data, here the board is the one being asked.
            For details, connection diagram and more, check out the example documentation at: <link placeholder>

@author     Soldered Electronics
"""

# The network module contains everything needed to join a Wi-Fi network.
import network

"""
The socket module is the lowest level of network communication: it lets us listen for other devices that want to talk
to us. MicroPython has no ready-made web server, so we build a small one out of a socket ourselves.
"""
import socket

# Pin controls the LED, and time gives us the pauses we need while connecting.
from machine import Pin
import time

"""
These two variables hold the name of your Wi-Fi network (the SSID) and its password. Replace the text between the
quotation marks with your own network details. Your phone or computer has to be on the same network as the board,
otherwise it will not be able to reach the page.
"""
ssid = "your ssid"
password = "your password"

"""
This is a variable to which we pass the number of pin that we had connected the LED to.
The NULA board has a pin naming logic as follows: IO4, where 4 is the number that we give to the variable.
If you wish to use a different pin, make sure you are using a IO__ marked pin.

Remember that the LED needs a 330 Ohm resistor in series with it. That resistor limits how much current flows, and
without it the LED draws more than either it or the pin is built for, so both can be damaged.
"""
LED_PIN = 4

"""
This is the name the board will try to claim on your network. If your network supports it, you can then open
http://nulamini.local/ in a browser instead of having to remember the address made of numbers.
"""
HOSTNAME = "nulamini"

"""
This is the web page itself, written in HTML and stored as one long piece of text. HTML is the language that
describes what a page looks like, the same language example.com sent us in the previous example.
The three quotation marks let us write many lines of text in one go, including single quotation marks, without having
to escape every one of them.
The page contains two buttons and a small piece of JavaScript, which is code that runs inside the browser and asks the
board for the current LED state every two seconds so the displayed status stays up to date on its own.
"""
HTML_PAGE = """<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>NULA MINI LED Control</title>
  <style>
    body { font-family: Arial; text-align: center; margin-top: 50px; }
    button { padding: 15px 30px; margin: 10px; font-size: 20px; }
    .status { font-size: 24px; margin-top: 20px; }
  </style>
</head>
<body>
  <h1>NULA MINI LED Control</h1>
  <button onclick="fetch('/led/on').then(()=>updateStatus())">ON</button>
  <button onclick="fetch('/led/off').then(()=>updateStatus())">OFF</button>
  <div class="status" id="status">Loading status...</div>

  <script>
    // Function that requests LED status from the NULA MINI and updates the page
    async function updateStatus() {
      let res = await fetch('/led/status');
      let text = await res.text();
      document.getElementById('status').innerHTML = 'LED is ' + text.toUpperCase();
    }

    // Run immediately after page load and update every 2 seconds
    updateStatus();
    setInterval(updateStatus, 2000);
  </script>
</body>
</html>"""

"""
Here we create our Pin object for the LED and immediately write 0 to it, so that the LED starts out switched off and
the status shown on the page matches reality.
"""
led = Pin(LED_PIN, Pin.OUT)
led.value(0)

"""
Here we create our network object and switch the Wi-Fi hardware on. network.STA_IF means the board joins someone
else's network, the same way your phone does.
"""
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

"""
Here we claim our name on the network. On most builds this also registers the name so that http://nulamini.local/
works from a browser. If it does not work on your network, use the address made of numbers that we print below.
We wrap it in a try block because not every firmware build offers this function, and a missing function should not
stop the whole example.
"""
try:
    network.hostname(HOSTNAME)
except Exception:
    print("Setting the hostname is not supported on this firmware, use the IP address instead.")

"""
connect() starts the connection attempt. It does not wait for the connection to finish, so we wait for it ourselves
in the loop below. isconnected() tells us whether we are online yet.
"""
print("Connecting to WiFi", end="")
wlan.connect(ssid, password)
while not wlan.isconnected():
    time.sleep(0.5)
    print(".", end="")

"""
ifconfig() returns the address the router handed out to our board as its first value. Typing this address into a
browser on the same network opens the page we prepared above.
"""
print()
print("WiFi connected!")
print("IP address:", wlan.ifconfig()[0])
print("Access the board in your browser at: http://" + HOSTNAME + ".local/")


def send_response(connection, content_type, body):
    """
    This is a function we wrote ourselves. It answers one request.
    Every HTTP answer starts with a few lines that describe it before the content itself: the response code, where 200
    means "here you go", and the type of the content we are sending. A blank line then separates those lines from the
    content.
    """
    connection.send("HTTP/1.1 200 OK\r\n")
    connection.send("Content-Type: " + content_type + "\r\n")
    connection.send("Connection: close\r\n\r\n")
    connection.sendall(body)


"""
Here we open the door and start listening. socket() creates the socket, setsockopt() lets us reuse the same port right
away when we restart the program instead of having to wait for the system to release it, bind() attaches us to port 80,
and listen() starts accepting connections.
A port is like a door number on the board: port 80 is the standard door for web pages, which is why browsers try it by
default and why we do not have to type it into the address bar.
"""
server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("", 80))
server.listen(2)
print("HTTP server started")

"""
We wrap the whole loop in a try block so that stopping the program with Ctrl+C, or with the stop button of your editor,
closes the socket properly instead of leaving it claimed.
"""
try:
    while True:

        """
        accept() waits until a browser connects to us. It gives us back two things: a connection we can talk over, and
        the address of whoever connected.
        """
        connection, address = server.accept()

        """
        recv() reads what the browser sent us, up to 1024 characters of it. The first line of any request names the
        address being asked for, which is what we need to decide how to answer.
        """
        request = connection.recv(1024).decode()
        first_line = request.split("\r\n")[0]

        """
        A request line looks like "GET /led/on HTTP/1.1", so splitting it on the spaces and taking the middle piece
        gives us the address on its own.
        """
        parts = first_line.split(" ")
        path = parts[1] if len(parts) > 1 else "/"

        """
        Here we decide what to do with each address. This is called routing: every address gets its own answer.
        The addresses starting with /led are the ones the buttons and the JavaScript in the page ask for, and they
        answer with a short piece of plain text rather than a whole page.
        """
        if path == "/led/on":
            led.value(1)
            print("LED ON")
            send_response(connection, "text/plain", "on")

        elif path == "/led/off":
            led.value(0)
            print("LED OFF")
            send_response(connection, "text/plain", "off")

        elif path == "/led/status":

            """
            value() reads back what the pin is currently writing, which tells us whether the LED is on. The if and
            else on one line is a short way of choosing between two values.
            """
            send_response(connection, "text/plain", "on" if led.value() else "off")

        else:

            # Any other address, including the plain "/", gets the web page itself.
            send_response(connection, "text/html", HTML_PAGE)

        """
        close() ends this one conversation. This matters: without it the browser would keep waiting and the board
        would slowly run out of memory.
        """
        connection.close()

except KeyboardInterrupt:

    # Stopping the program closes the door behind us, so the port is free the next time we start.
    print("Server stopped")
    server.close()
