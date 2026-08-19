"""
@file       6.3_Sending_Data.py
@brief      Example that shows how to send data from the NULA board to a server on the internet using an HTTP POST
            request. Every few seconds the board makes up a random number and sends it to a webhook, which is a
            web address that simply collects whatever is sent to it and shows it to you in your browser.
            In example 6.1 we read data from the internet, here we write data to it.
            For details, connection diagram and more, check out the example documentation at: <link placeholder>

@author     Soldered Electronics
"""

# The network module contains everything needed to join a Wi-Fi network.
import network

# The urequests module lets us speak HTTP, the language browsers use to talk to websites.
import urequests

# The random module can make up numbers for us, which stands in for a real sensor reading in this example.
import random
import time

"""
These two variables hold the name of your Wi-Fi network (the SSID) and its password. Replace the text between the
quotation marks with your own network details.
"""
ssid = "your ssid"
password = "your password"

"""
This variable holds the address we send our data to. Open https://webhook.site in a browser, copy the unique link it
shows you at the top of the page, and paste it between the quotation marks below. Keep that browser tab open and you
will see every value the board sends appear in it.
Example: https://webhook.site/your-unique-id
"""
webhook_url = "your unique url"

"""
This variable defines how much time passes between two messages, in milliseconds. 5000 milliseconds is five seconds.
Feel free to experiment with this value, but be aware that sending data very often is impolite towards whichever
server is receiving it.
"""
POST_INTERVAL_MS = 5000

"""
This variable remembers the moment when we sent the last message, so we know when the next one is due.
"""
last_post = 0

"""
seed() gives the random number generator a starting point. Handing it the current value of the microsecond clock means
the numbers differ after every reset, rather than repeating the same sequence, which is easy to mistake for a broken
program.
"""
random.seed(time.ticks_us())

print()
print("Wi-Fi POST Request Example")

"""
Here we create our network object and switch the Wi-Fi hardware on. network.STA_IF means the board joins someone
else's network, the same way your phone does.
"""
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

"""
connect() starts the connection attempt using the network name and password we defined above. It does not wait for the
connection to finish, so we wait for it ourselves in the loop below, printing one dot every half second so we can see
the board is still trying.
"""
wlan.connect(ssid, password)
print("Connecting to Wi-Fi", end="")
while not wlan.isconnected():
    time.sleep(0.5)
    print(".", end="")

# ifconfig() returns the address the router handed out to our board as its first value.
print()
print("Connected to Wi-Fi!")
print("IP Address:", wlan.ifconfig()[0])

while True:

    """
    time.ticks_ms() is a function that returns the number of milliseconds passed since the board was powered on. We use
    it instead of a plain sleep so the board stays free to do other work between messages.
    """
    now = time.ticks_ms()

    """
    Here we check how much time has passed since the last message. Only when POST_INTERVAL_MS milliseconds have gone by
    do we send a new one, and we immediately remember the current time as the new starting point.
    """
    if time.ticks_diff(now, last_post) >= POST_INTERVAL_MS:
        last_post = now

        """
        Before sending anything we check that we are still online. A Wi-Fi connection can drop at any time, and trying
        to send data without one would only waste time and print errors.
        """
        if wlan.isconnected():

            """
            randint() returns a whole random number, and both of the values we give it are included, so this gives us a
            number from 0 to 100.
            In a real project this is where a sensor reading would go.
            """
            random_number = random.randint(0, 100)

            """
            Here we build the data we are going to send. The format "name=value" is the same one a browser uses when
            you submit a simple web form, and str() turns our number into text so it can be joined to the rest.
            """
            post_data = "number=" + str(random_number)

            print("----------------------------------")
            print("Sending POST request to webhook.site...")
            print("Data:", post_data)

            """
            We wrap the request in a try block because anything that goes over a network can fail, and without it a
            failed request would stop the whole program with an error.
            """
            try:

                """
                post() sends the request together with our data and waits for the answer. POST is the HTTP method used
                for sending data to a server, while GET, which we used in example 6.1, is the one used for reading data
                from it.
                The headers we pass along describe the format our data is written in, so the server knows how to read
                it. A header is one line of extra information about the request itself.
                """
                response = urequests.post(
                    webhook_url,
                    data=post_data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )

                """
                status_code is the number the server answers with. 200 means "here you go", and anything from 400
                upwards means something went wrong. text is the body of the answer.
                """
                print("Server response code:", response.status_code)
                print("Response body:")
                print(response.text)

                """
                close() releases the memory the response was using. Always close a response once you are done with it,
                otherwise a program that makes many requests will slowly run out of memory.
                """
                response.close()

            except Exception as e:

                # If anything went wrong, print the reason instead of letting the program stop.
                print("POST failed. Error:", e)

        else:

            # If we lost the connection, start a new attempt and try again on the next pass.
            print("Wi-Fi not connected. Trying to reconnect...")
            wlan.connect(ssid, password)

    # A very short pause leaves the processor a moment to handle its own background work.
    time.sleep_ms(10)
