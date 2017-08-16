class Accelerator:
    maxSpeed = False
    minSpeed = False
    midSpeed = False
    step = 10

    curSpeed = False

    def __init__(self, config, mainWindow):
        pass

    def speedUp(self):
        self.curSpeed = self.curSpeed + self.step

    def speedDown(self):
        self.curSpeed = self.curSpeed - self.step

    def brake(self):
        self.curSpeed = self.midSpeed

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
