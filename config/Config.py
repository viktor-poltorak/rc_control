import configparser, os, re


class Config:
    __configFileName = "config.ini"
    __parser = None
    __MainSectionName = "Global"
    # Available option
    title = "Title"
    steeringMid = 1500
    accelerateMid = 1500
    brake = 1500
    tty = None
    baudrate = None
    udp_port = 5555
    tcp_port = 5555

    def __init__(self, fileName="config.ini"):
        self.__configFileName = fileName
        self.__parser = configparser.RawConfigParser()

        if not os.path.exists(fileName):
            with open(fileName, "w") as f:
                f.close();

        self.__parser.read(fileName)
        self._readOptions(self.__MainSectionName);

    # Write config back
    def write(self):
        with open(self.__configFileName, "w") as f:
            self.__parser.write(f)
            f.close();

    def getOption(self, name):
        return getattr(self, name, None)

    # Set option
    def setOption(self, name, value, section=None):
        if section is None:
            section = self.__MainSectionName

        self.__parser.set(section, name, value);

    # Read options
    def _readOptions(self, sectionName):
        if not self.__parser.has_section(sectionName):
            self.__parser.add_section(sectionName);

        for option in self.__parser.options(sectionName):
            if hasattr(self, option):
                setattr(self, option, self.__parser.get(sectionName, option))

    # Get dist of options
    def getOptions(self):
        list = [a for a, v in Config.__dict__.items()
                if not re.match('<function.*?>', str(v))
                and not a.startswith('_')]
        result = {}
        for key in list:
            result[key] = getattr(self, key)
        return result
