class Accelerator:
    commandKey = "A"
    # Accelerate
    accelerateMid = 1500
    brakePos = 1500

    maxSpeed = False
    minSpeed = False
    midSpeed = False
    step = 10

    connection = None
    curPos = False

    def __init__(self, config, connection):
        """
        :param config: Config
        :param connection: Used to send commands (in current case it is main window object
        """
        self.accelerateMid = int(config.accelerateMid)
        self.curPos = self.accelerateMid
        self.brakePos = int(config.brake)
        self.connection = connection
        pass

    def sendCommand(self, command):
        """
        Decorator for send commands
        :param command: string
        :return:
        """
        self.connection.sendCommand(command)

    def speedUp(self):
        self.curPos = int(self.curPos) + int(self.step)
        self.sendCommand(self.getCommand())

    def speedDown(self):
        self.curPos = int(self.curPos) - int(self.step)
        self.sendCommand(self.getCommand())

    def brake(self):
        self.curPos = int(self.brakePos)
        self.sendCommand(self.getCommand())
        self.curPos = self.accelerateMid

    def backward(self):
        self.brake();
        command = "{}:{};{}:{};{}:{};".format(self.commandKey, self.accelerateMid + 360,
                                              self.commandKey, self.accelerateMid,
                                              self.commandKey, self.accelerateMid - 170)
        self.sendCommand(command)
        # self.curPos = self.accelerateMid
        # self.sendCommand(self.getCommand())

    def forward(self):
        if self.curPos < (self.accelerateMid + 100):
            startSpeed = self.accelerateMid + 130
            command = "{}:{};{}:{};".format(self.commandKey, self.brakePos,
                                                  self.commandKey, startSpeed)
            self.sendCommand(command)
            self.curPos = startSpeed

    def getRawPos(self):
        return self.curPos

    def getCommand(self) -> str:
        return "{}:{};".format(self.commandKey, self.getRawPos())
