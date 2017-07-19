#!/usr/bin/python3
# Test

import socket
import time
import sys

# bind all IP
HOST = '0.0.0.0'
# Listen on Port
PORT = 5555
# Size of receive buffer
BUFFER_SIZE = 1024

iterations = 1

# Create a TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the host and port
s.bind((HOST, PORT))
while iterations > 0:
    print("Begin iteration ", iterations)
    # Receive BUFFER_SIZE bytes data
    # data is a list with 2 elements
    # first is data
    # second is client address
    data = s.recvfrom(BUFFER_SIZE)
    if data:
        # print received data
        print('Client to Server: ', data)
        # Convert to upper case and send back to Client
        s.sendto(b"IT IS ME", data[1])
    time.sleep(2)
    iterations -= 1

# Close connection
s.close()

#Next tcp server