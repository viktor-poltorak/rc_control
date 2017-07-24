import asyncio, socket

port = 5555


def getIP():
    '''
    Return IP address
    :param self:
    :return:
    '''
    return "127.0.0.1"
    return [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in
            [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]


class EchoClientProtocol:
    isRun = True

    def __init__(self, message, loop):
        self.message = message
        self.loop = loop
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

        while self.isRun :
            message = input(">>")
            print('Send:', message)
            self.transport.sendto(message.encode())

    def datagram_received(self, data, addr):
        print("Received:", data.decode())

        print("Close the socket")
        self.transport.close()

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print("Socket closed, stop the event loop")
        loop = asyncio.get_event_loop()
        loop.stop()


loop = asyncio.get_event_loop()
message = "board_1"
connect = loop.create_datagram_endpoint(
    lambda: EchoClientProtocol(message, loop),
    remote_addr=(getIP(), port))
transport, protocol = loop.run_until_complete(connect)

try:
    loop.run_forever()
except KeyboardInterrupt:
    transport.close()
    loop.close()
