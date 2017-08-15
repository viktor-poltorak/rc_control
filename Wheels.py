class Wheels:
    _midPos = False
    _leftPos = False
    _rightPos = False
    _curPos = False

    POS_MID = 1
    POS_LEFT = 2
    POS_RIGHT = 3

    def __init__(self, midPos, leftPos, rightPos):
        self._midPos = midPos
        self._rightPos = rightPos
        self._leftPos = leftPos
        self._curPos = midPos

    def turnLeft(self):
        self._curPos = self._leftPos

    def turnRight(self):
        self._curPos = self._rightPos

    def resetPos(self):
        self._curPos = self._midPos

    def getRawPos(self):
        return self._curPos

    def getCommand(self) -> str:
        return "{}:{};".format('S', self.getRawPos())

    def getPos(self) -> int:
        if self._curPos == self._leftPos:
            return self.POS_LEFT
        if self._curPos == self._rightPos:
            return self.POS_RIGHT

        return self.POS_MID
