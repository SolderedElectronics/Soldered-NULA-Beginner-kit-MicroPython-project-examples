"""
@file       6.1_Connecting_and_Getting_Data.py
@brief      Example that shows how to connect the NULA board to a Wi-Fi network and then ask a website for data.
            The board makes an HTTP GET request to example.com and prints whatever the website sends back to the
            console. This is the first step towards any project that needs data from the internet.
            For details, connection diagram and more, check out the example documentation at: <link placeholder>

@author     Soldered
"""

"""
The network module contains everything needed to join a Wi-Fi network. It is built into MicroPython, so there is
nothing to install for this one.
"""
import network

"""
The urequests module lets us speak HTTP, the language browsers use to talk to websites. Without it we would have to
build the requests out of raw text ourselves.
"""
import urequests
import time

"""
These two variables hold the name of your Wi-Fi network (the SSID) and its password. Replace the text between the
quotation marks with your own network details, otherwise the board has nothing to connect to.
Note that most boards, including the NULA board, can only connect to 2.4 GHz networks and not to 5 GHz ones.
"""
ssid = "your ssid"
password = "your password"

"""
This is the address we want to visit. A URL is the same kind of address you type into a browser, and example.com is a
small page that exists for exactly this kind of testing.
"""
url = "http://example.com/"

print()
print("Wi-Fi GET Request Example")

"""
Here we create our network object, which we named "wlan". network.STA_IF means we want the board to behave as a
station, which is the name for a device that joins someone else's network, the same way your phone does.
"""
wlan = network.WLAN(network.STA_IF)

"""
active() switches the Wi-Fi hardware on, and connect() starts the connection attempt using the network name and
password we defined above. connect() does not wait for the connection to finish, it only starts the process.
"""
wlan.active(True)
wlan.connect(ssid, password)
print("Connecting to Wi-Fi", end="")

"""
Because connect() returns immediately, we have to wait for the connection ourselves. isconnected() tells us whether
we are online yet. This while loop keeps running as long as we are not connected, printing one dot every half second
so we can see that the board is still trying.
"""
while not wlan.isconnected():
    time.sleep(0.5)
    print(".", end="")

"""
Once we are through the loop above, we are connected. ifconfig() returns four values: the address the router handed
out to our board, the subnet mask, the gateway and the DNS server. The first of those is the one we care about here,
so write it down, we will need it in the next example.
"""
print()
print("Connected to Wi-Fi!")
print("IP Address:", wlan.ifconfig()[0])

print("Requesting data from:", url)

"""
get() sends the request and waits for the website to answer. GET is the HTTP method used for reading data, which is
exactly what a browser does every time you open a page.
We wrap this in a try block because anything that goes over a network can fail, and without it a failed request would
stop the whole program with an error.
"""
try:
    response = urequests.get(url)

    """
    status_code is the number the server answers with. 200 means "here you go", and anything from 400 upwards means
    something went wrong. text is the content of the page itself, which for example.com is its HTML.
    """
    print("HTTP Response Code:", response.status_code)
    print("Received data:")
    print("----------------------------------")
    print(response.text)
    print("----------------------------------")

    """
    close() releases the memory the response was using. Always close a response once you are done with it, otherwise
    a program that makes many requests will slowly run out of memory.
    """
    response.close()

except Exception as e:

    # If anything went wrong, print the reason instead of letting the program stop.
    print("Request failed. Error:", e)

"""
And that is all. Unlike the earlier examples there is no while True loop here, because we only wanted to make the one
request.
"""
