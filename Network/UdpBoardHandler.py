import functools, re

from PyQt5.QtNetwork import QUdpSocket
from PyQt5.QtWidgets import QTextEdit
from Network.Nettool import get_ip
from config.Config import Config


class UdpBoardHandler:
    """
    Handle board by udp connection
    """
    udpSocket = None
    console = None
    config = None

    def __init__(self, socket: QUdpSocket, console: QTextEdit, handler, config):
        """
        :param socket: QUdpSocket
        :param console: QTextEdit
        :param handler: function
        """
        self.udpSocket = socket
        self.console = console
        self.handler = functools.partial(handler)
        self.config = config

    def handle_board(self):
        '''

        :return:None
        '''
        while self.udpSocket.hasPendingDatagrams():
            datagram, host, port = self.udpSocket.readDatagram(self.udpSocket.pendingDatagramSize())
            self.console.append("Message from {}:{}".format(host.toString(), port))
            print(datagram)
            try:
                datagram = str(datagram, encoding='utf8')
                # self.console.append("Udp msg from {}".format(host))

                pattern = re.compile("^board_\d+$")  # Check for board
                if pattern.match(datagram):
                    self.console.append("Board found")
                    message = "TCP:{}:{}".format(get_ip(), self.config.getOption('tcp_port'))
                    self.console.append(message)
                    self.udpSocket.writeDatagram(message.encode(), host, port)
                    self.handler(host, port)
                else:
                    self.console.append("Wrong board")
                    self.udpSocket.writeDatagram(b"FAIL", host, port)
            except TypeError:
                pass
