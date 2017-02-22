import sys, serial
from serial import serialutil


class ConnectorBus:
    __conn = None
    __tty = None
    __baudrate = None
    errorMessage = None

    def __init__(self, tty, baudrate):
        self.__tty = tty
        self.__baudrate = baudrate

    @property
    def isConnected(self):
        if self.__conn is None:
            return False

        return self.__conn.isOpen()

    def disconnect(self):
        if self.__conn is None:
            return False
        return self.__conn.close()

    def connect(self):
        try:
            self.__conn = serial.Serial(self.__tty, baudrate=self.__baudrate)
            self.__conn.open()
            self.__conn.flushInput()
            self.__conn.flushOutput()
        except Exception as ex:
            print("Unexpected error: " + format(ex))
            self.errorMessage = format(ex)

    def getErrorMessage(self):
        return str(self.errorMessage)

    def send(self, command):
        self.__conn.write(bytes(command + "\r\n", "utf-8"))

        self.__conn.flush()

    def read(self):
        if self.__conn.inWaiting():
            return self.__conn.readline().decode()
