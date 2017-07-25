from PyQt5.QtNetwork import QUdpSocket, QHostAddress
from functools import partial


class Server():
    _ip = None
    _port = None
    udpSocket = None
    callback = None
    _isRunning = True

    def __init__(self, ip="127.0.0.1", port=9999):
        self._ip = ip
        self._port = port
        self.callback = lambda datagram, host, port: print(
            "Recieved {} from {}:{}".format(datagram, host, port))  # default callback

    def start(self, window):
        self.udpSocket = QUdpSocket(window)
        self.udpSocket.bind(QHostAddress(self._ip), self._port)
        self.udpSocket.readyRead.connect(self.data_handler)
        print("Udp server started at {}:{}".format(self._ip, self._port))

    def set_callback(self, callback):
        self.callback = partial(callback)

    def data_handler(self):
        while self.udpSocket.hasPendingDatagrams():
            print("Recieved data")
            datagram, host, port = self.udpSocket.readDatagram(self.udpSocket.pendingDatagramSize())
            try:
                # Python v3.
                datagram = str(datagram)
                self.callback(datagram, host, port)
            except TypeError:
                # Python v2.
                pass

    def send_message(self, message, host=False, port=False):
        if not host:
            host = QHostAddress(QHostAddress.Broadcast)
        else:
            host = QHostAddress(host)

        if not port:
            port = self._port

        self.udpSocket.writeDatagram(message.encode(), host, port)

    def close_connection(self):
        print("Udp Connection closed")
        self.udpSocket.close()
