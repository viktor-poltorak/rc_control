import functools, re

from PyQt5.QtNetwork import QUdpSocket
from PyQt5.QtWidgets import QTextEdit


class UdpBoardHandler:
    """
    Handle board by udp connection
    """
    udpSocket = None
    console = None

    def __init__(self, socket: QUdpSocket, console: QTextEdit, handler):
        """
        :param socket: QUdpSocket
        :param console: QTextEdit
        :param handler: function
        """
        self.udpSocket = socket
        self.console = console
        self.handler = functools.partial(handler)

    def handle_board(self):
        '''

        :return:None
        '''
        while self.udpSocket.hasPendingDatagrams():
            datagram, host, port = self.udpSocket.readDatagram(self.udpSocket.pendingDatagramSize())
            try:
                datagram = str(datagram, encoding='utf8')
                pattern = re.compile("^board_\d+$")  # Check for board
                if pattern.match(datagram):
                    self.udpSocket.writeDatagram(b"OK", host, 5555)
                    self.console.append("Board found")
                    self.handler(host, port)
                else:
                    self.console.append("Wrong board")
            except TypeError:
                pass
