#!/usr/bin/python3

import socket
from Finder.UdpFinder import UdpFinder

port = 5555
def getIP():
    '''
    Return IP address
    :param self:
    :return:
    '''
    return [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in
            [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]

finder = UdpFinder(getIP(), port)

print(finder.get_version())
finder.start();
