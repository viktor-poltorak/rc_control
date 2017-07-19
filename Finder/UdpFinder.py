import asyncio


class UdpFinder:
    _version = 1
    _ip = None
    _port = None

    def __init__(self, ip="127.0.0.1", port=9999):
        self._ip = ip
        self._port = port

    def get_version(self):
        return self._version

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        message = data.decode()
        print('Received %r from %s' % (message, addr))
        print('Send %r to %s' % (message, addr))
        self.transport.sendto(data, addr)

    def start(self):
        loop = asyncio.get_event_loop()
        print("Starting UDP server")
        # One protocol instance will be created to serve all client requests
        listen = loop.create_datagram_endpoint(UdpFinder, local_addr=(self._ip, self._port))
        transport, protocol = loop.run_until_complete(listen)
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass

        transport.close()
        loop.close()
