import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QTextEdit
from PyQt5.QtCore import QBasicTimer

from config.Config import Config
from ConnectorBus.ConnectorBus import ConnectorBus


class MainWindow(QMainWindow):
    config = None
    _connection = None

    def __init__(self):
        super().__init__()

        self.config = Config("config.ini")
        self.__initUI()
        self.show()

    def __initUI(self):
        # Set up the user interface from Designer.
        uic.loadUi("main.ui", self)
        self.debug()
        # Connect up the buttons.
        self.connectButton.clicked.connect(self.onConnect)
        self.sendButton.clicked.connect(self.onSend)
        self.timer = QBasicTimer()
        self.timer.start(100, self)

    def onConnect(self):
        self._connection = ConnectorBus(self.config.getOption('tty'), self.config.getOption('baudrate'))
        self._connection.connect()

        if self._connection.isConnected:
            self.statusBar().showMessage("Connected")
            self.connectButton.setEnabled(False)
        else:
            self.statusBar().showMessage("Not connected " + self._connection.getErrorMessage())
            self.connectButton.setEnabled(True)

    def onSend(self):
        command = self.query.text()

        if not command:
            return None

        self._connection.send(command)
        self.console.append(command)
        self.query.setText("")

    def timerEvent(self, e):
        self.updateConsole()

    def updateConsole(self):
        if not self._connection:
            return

        response = self._connection.read()
        print(response)
        if response:
            self.console.append(response)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.disconnect()
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
