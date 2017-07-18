import socket

class Finder:
    statusBar = None
    config = None
    enableFinding = False
    bindIp = '192.169.255.255'
    port = 5555

    def __init__(self, statusBar, config):
        self.statusBar = statusBar
        self.config = config

    def startFinding(self):
        self.statusBar.showMessage("Finding board...");

    def startUpdSearching(self):
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind the socket to the port
        server_address = ('localhost', self.port)
        print('starting up on {} port {}'.format(*server_address))
        sock.bind(server_address)

        while True:

            data, address = sock.recvfrom(4096)

            print('received {} bytes from {}'.format(
                len(data), address))
            print(data)

            if data:
                sent = sock.sendto(data, address)
                print('sent {} bytes back to {}'.format(
                    sent, address))
        None
