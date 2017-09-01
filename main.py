import sys

from PyQt5.QtGui import QPixmap

from Wheels import Wheels
from Accelerator import Accelerator
from PyQt5 import uic
from PyQt5.QtCore import QBasicTimer, Qt, QDataStream
from PyQt5.QtWidgets import QMainWindow, QApplication
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
    wheels = None
    accelerator = None

    def __init__(self):
        super().__init__()
        self.config = Config("config.ini")

        # INIT Controls
        self.wheels = Wheels(self.config.steeringMid, self.config.steeringLeft, self.config.steeringRight)
        self.accelerator = Accelerator(self.config, self)

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

        self.updateWheelsImage()
        # Connect up the buttons.
        # self.connectButton.clicked.connect(self.onConnect)
        self.query.returnPressed.connect(self.onSend)
        self.sendButton.clicked.connect(self.onSend)
        self.clearLogButton.clicked.connect(self.onClearLog)
        self.debugButton.clicked.connect(self.onDebug)
        self.timer = QBasicTimer()
        self.timer.start(100, self)

    def updateWheelsImage(self):
        pos = self.wheels.getPos()
        image = 'res/flat_wheel.png'

        if pos == self.wheels.POS_LEFT:
            image = 'res/left_wheel.png'
        if pos == self.wheels.POS_RIGHT:
            image = 'res/right_wheel.png'
        # Create widget
        pixmap = QPixmap(image)
        self.wheelsImage.setPixmap(pixmap)
        self.wheelsImage.setFixedWidth(pixmap.width())
        self.wheelsImage.setFixedHeight(pixmap.height())
        self.show()

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
        cmd = cmd.strip()
        self._log("Send: {}".format(cmd))

        if self.board_connection.__class__.__name__ != 'NoneType':
            self.board_connection.write(cmd.encode())
        else:
            self._log("Unable send command. No connection")

    def keyPressEvent(self, event):
        '''
        A - left
        D - right
        S - wheel mid
        Up - speed up
        Down - speed down
        Space - break
        :param event:
        :return:
        '''
        if event.key() == Qt.Key_A:
            self.wheels.turnLeft()
            self.sendCommand(self.wheels.getCommand())

        if event.key() == Qt.Key_D:
            self.wheels.turnRight()
            self.sendCommand(self.wheels.getCommand())

        if event.key() == Qt.Key_S:
            self.wheels.resetPos()
            self.sendCommand(self.wheels.getCommand())

        if event.key() == Qt.Key_Space:
            self.accelerator.brake()

        if event.key() == Qt.Key_Up:
            self.accelerator.speedUp()

        if event.key() == Qt.Key_Down:
            self.accelerator.speedDown()

        self.updateWheelsImage()

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

        self.sendCommand(command)
        self.query.setText("")

    def onClearLog(self):
        self.console.setText('')

    def onDebug(self):
        options = self.config.getOptions()
        self._log("*********** DEBUG ************")
        self._log("Wheels:{}".format(self.wheels.getRawPos()))
        if self.board_connection.__class__.__name__ != 'NoneType':
            self._log("Rc car IP:{}:{}".format(self.board_connection.localAddress(), self.board_connection.localPort()))
            # for key in options:
            #    self._log(key + "=" + str(options[key]))
        self._log("******************************")

    def timerEvent(self, event):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.config.write()

    def _log(self, message):
        print(message)
        self.console.append(message)


class CommandHelper:
    @staticmethod
    def getCommand(mode, value):
        return "%s:%s;".format(mode, value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
