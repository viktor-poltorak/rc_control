import sys, signal
from PyQt5 import uic
from PyQt5.QtCore import QBasicTimer, Qt, QDataStream
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5.QtNetwork import QUdpSocket, QHostAddress, QTcpServer

from config.Config import Config
from Network.Nettool import get_ip
from Network.UdpBoardHandler import UdpBoardHandler


class MainWindow(QMainWindow):
    config = None
    udpSocket = None
    tcpServer = None
    tcpBoard = None
    board_connection = None

    def __init__(self):
        super().__init__()

        self.config = Config("config.ini")
        self.__initUI()
        self.statusBar().showMessage("Board not connected")

        # Init uds listener
        self._log("Init udp at {}:{}".format(get_ip(), self.config.getOption('udp_port')))
        self.udpSocket = QUdpSocket()
        self.udpSocket.setLocalAddress(QHostAddress(get_ip()))
        self.udpSocket.bind(self.config.getOption('udp_port'))
        self.udpSocket.readyRead.connect(self.udpHandler)

        # Init tcp server
        self.tcpServer = QTcpServer(self)
        self._log("Starting TCP at {}:{} ".format(get_ip(), str(self.config.getOption('tcp_port'))))
        self.tcpServer.listen(QHostAddress(get_ip()), self.config.getOption('tcp_port'))
        self.tcpServer.newConnection.connect(self.establishBoardConnection)

        self.show()

    def __initUI(self):
        # Set up the user interface from Designer.
        uic.loadUi("main.ui", self)
        self.debug()
        # Connect up the buttons.
        # self.connectButton.clicked.connect(self.onConnect)
        self.query.returnPressed.connect(self.onSend)
        self.sendButton.clicked.connect(self.onSend)
        self.timer = QBasicTimer()
        self.timer.start(100, self)

    def udpHandler(self):
        udp_handler = UdpBoardHandler(self.udpSocket, self.console, self.handleBoard, self.config)
        udp_handler.handle_board();

    def handleBoard(self, host: QHostAddress, port):
        message = "Board found at {}:{}".format(host.toIPv4Address(), port)
        self._log(message)

    def establishBoardConnection(self):
        self.board_connection = self.tcpServer.nextPendingConnection()
        self.board_connection.readyRead.connect(self.messageFromBoard)
        self._log("board here")

    def messageFromBoard(self):
        instr = QDataStream(self.board_connection)
        instr.setVersion(QDataStream.Qt_5_0)
        if self.board_connection.bytesAvailable() > 0:
            self._log(str(self.board_connection.readAll()));

    def sendCommand(self, cmd):
        self._log("Send: {}".format(cmd))
        self.board_connection.write(cmd.encode())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            self.sendCommand("S:1800;")

        if event.key() == Qt.Key_D:
            self.sendCommand("S:1300;")

        if event.key() == Qt.Key_S:
            self.sendCommand("S:1500;")

    def onButtonUp(self):
        print("up")
        pass

    def onButtonDown(self):
        print("down")
        pass

    def onSend(self):
        command = self.query.text()

        if not command:
            return None

        self.board_connection.write(command.encode())
        self.console.append(command)
        self.query.setText("")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.config.write()

    def debug(self):
        options = self.config.getOptions()
        startPos = 10

        for key in options:
            label = QLabel(self)
            label.move(0, startPos)
            text = key + "=" + str(options[key])
            label.setText(text)
            label.adjustSize()
            startPos += 20

    def _log(self, message):
        print(message)
        self.console.append(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
