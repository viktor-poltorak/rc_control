from PyQt5.QtNetwork import QTcpSocket
from typing import Type


class TcpBoardHandler:
    """
    Handle board via tcp
    """
    board_connection = Type[QTcpSocket]

    def __init__(self, board_connection: QTcpSocket):
        self.board_connection = board_connection

    def send(self, message):
        self.board_connection.write(str(message).encode())

        if self.board_connection.bytesAvailable() > 0:
            resp = self.board_connection.readAll()
            resp = str(resp, encoding="utf8")
            if resp == "OK":
                return True
            else:
                return False
