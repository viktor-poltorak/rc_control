#!/usr/bin/python3

import socket
import asyncio
from Udp.Server import Server
import time


class Controller:
    udp_server = None
    port = 5555

    def get_ip(self):
        '''
        Return IP address
        :param self:
        :return:
        '''
        return [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in
                [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]

    def callback(self, data, host, port):
        print("Callback. {} {} {}".format(data, host, port))

    def __init__(self):
        self.udp_server = Server(self.get_ip(), self.port)
        # self.udp_server.set_callback(self.callback)
        self.udp_server.start();

    def some_action(self, message=''):
        self.udp_server.send_message(message)

    def close_connection(self):
        self.udp_server.close_connection()


if __name__ == '__main__':
    controller = Controller()

    try:
        pass
        #while True:
            #controller.udp_server.data_handler()
            #time.sleep(1)
        #    msg = input(">>")
        #    controller.some_action(msg)
    except KeyboardInterrupt:
        controller.close_connection()
    finally:
        controller.close_connection()
