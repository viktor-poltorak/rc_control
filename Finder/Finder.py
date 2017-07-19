import socket
import sys
import traceback


class Finder:
    '''
    Idea: implement net methods with asyncio
    '''
    statusBar = None
    enableFinding = False
    port = 5555
    boardConnection = None

    def __init__(self, statusBar, config):
        self.statusBar = statusBar
        self.config = config
        if config.setOption('port', 'Network'):
            self.port = config.getOption('port', 'Network')

    def startFinding(self):
        self.statusBar.showMessage("Finding board...")
        self.startUpdSearching()

    @staticmethod
    def getIP():
        '''
        Return IP address
        :param self:
        :return:
        '''
        return [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in
                [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]

    def startUpdSearching(self):
        # Create a TCP/IP socket
        soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind the socket to the host and port

        soc.bind((self.getIP(), self.port))  # Receive BUFFER_SIZE bytes data
        # data is a list with 2 elements
        # first is data
        # second is client address
        soc.setblocking(0)
        data = soc.recvfrom(1024)
        if data:
            # print received data
            self.statusBar.showMessage("Board found on ", str(data))
            # Convert to upper case and send back to Client
            soc.sendto(b"IT IS ME", data[1])
        # Close connection
        soc.close()

    def startTcpListener(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # this is for easy starting/killing the app
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print('Socket created')

        try:
            soc.bind((self.getIP(), self.port))
            print('Socket bind complete')
        except socket.error as msg:
            print('Bind failed. Error : ' + str(sys.exc_info()))
            return False

        # Start listening on socket
        soc.listen(1)
        self.statusBar.showMessage('Waiting for connection...')

        # For now one connection is ok
        conn, addr = soc.accept()

        ip, port = str(addr[0]), str(addr[1])
        print('Accepting connection from ' + ip + ':' + port)
        try:
            self.clientProcess(conn, ip, port)
        except:
            self.statusBar.showMessage("Terible error!")
            traceback.print_exc()
            return False

    def clientProcess(self, conn, ip, port, MAX_BUFFER_SIZE=4096):
        # the input is in bytes, so decode it
        clientResponseBytes = conn.recv(MAX_BUFFER_SIZE)

        # MAX_BUFFER_SIZE is how big the message can be
        # this is test if it's sufficiently big

        size = sys.getsizeof()
        if size >= MAX_BUFFER_SIZE:
            print("The length of input is probably too long: {}".format(size))

        # decode input and strip the end of line
        clientResponse = clientResponseBytes.decode("utf8").rstrip()
        if clientResponse == 'OK':
            self.boardConnection = conn

    def getConnection(self):
        return self.boardConnection

    def closeConnection(self):
        self.boardConnection.close()
