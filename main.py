import sys, signal
from PyQt5 import uic
from PyQt5.QtCore import QBasicTimer, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5.QtNetwork import QUdpSocket, QHostAddress

from config.Config import Config
from Network.Nettool import get_ip
from Network.UdpBoardHandler import UdpBoardHandler


class MainWindow(QMainWindow):
    config = None
    udpSocket = None

    def __init__(self):
        super().__init__()

        self.config = Config("config.ini")
        self.__initUI()
        self.statusBar().showMessage("Board not connected")

        # Init uds listener
        print("Init udp")
        self.udpSocket = QUdpSocket()
        self.udpSocket.setLocalAddress(QHostAddress(get_ip()))
        self.udpSocket.bind(5555)
        self.udpSocket.readyRead.connect(self.udpHandler)

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
        udp_handler = UdpBoardHandler(self.udpSocket, self.console, self.processTcpConnection)
        udp_handler.handle_board();

    def processTcpConnection(self, host, port):
        print("Ura", host, port)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            self._connection.send("S:1800;")

        if event.key() == Qt.Key_D:
            self._connection.send("S:1300;")

        if event.key() == Qt.Key_S:
            self._connection.send("S:1500;")

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

        self.console.append(command)
        self.query.setText("")

    def updateConsole(self):
        response = "DATA"
        print(response)
        if response:
            self.console.append(response)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
