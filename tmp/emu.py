import asyncio

import sys, socket
import threading

controller_ip = ('192.168.100.2', 5555)

def udpProcess():
    global controller_ip
    UDP_HOST = ''
    UDP_PORT = 5555

    def print_response(conn, e):
        global controller_ip
        conn.bind(('0.0.0.0', 5556))
        print("Init udp reader")
        while True:
            data, addr = conn.recvfrom(1024)
            data = str(data, encoding="utf8")
            print("Udp resp: ", data.strip())

            if data.find("TCP") > -1:
                protocol, ip, port = data.split(":")
                controller_ip = (ip, int(port))
                print("Controller addr: ", controller_ip)
                e.set()
                break

    print("Start udp part")
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    event = threading.Event()
    printRespThread = threading.Thread(target=print_response, args=(sock, event))
    printRespThread.start()

    while True:
        if event.is_set():
            print("Start TCP controller addr ", controller_ip)
            break

        cmd = input("udp>")
        if not cmd:
            continue

        if cmd == "exit":
            print("Stop udp part")
            break;

        sock.sendto(cmd.encode(), (UDP_HOST, UDP_PORT))

    print("Close udp connection")
    sock.close()


def tcpProcess():
    print("Start tcp part")

    if not controller_ip:
        print("No controller")
        return False

    def print_response(conn):
        print("Init tcp reader")
        while True:
            data, addr = conn.recvfrom(1024)
            data = str(data, encoding="utf8")
            print("Tcp resp: ", data.strip())

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect(controller_ip)


    printRespThread = threading.Thread(target=print_response, args=(tcp_socket,))
    printRespThread.start()

    try:
        while True:
            cmd = input("tcp>")

            if not cmd:
                continue
            if cmd == "exit":
                print("Stop tcp part")
                break

            tcp_socket.sendall(cmd.encode())
    except KeyboardInterrupt:
        print("Close tcp connection")

    tcp_socket.close()
    print("Close tcp connection")


def main():
    print("Board Emulator v1")

    while True:
        cmd = input(">>")

        if not cmd:
            continue

        print("Run command: ", cmd)
        if cmd == 'udp':
            udpProcess()

        if cmd == 'tcp':
            tcpProcess()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Buy buy")
        print("Close resources")
sys.exit()


# TCP client
class TcpClient(asyncio.Protocol):
    message = 'Testing'

    def connection_made(self, transport):
        self.transport = transport
        self.transport.write(self.message.encode())
        print('data sent: {}'.format(self.message))
        # server_udp[1].tcp_client_connected()

    def data_received(self, data):
        self.data = format(data.decode())
        print('data received: {}'.format(data.decode()))
        # if self.data == 'Testing':
        # server_udp[1].send_data_to_udp(self.data)

    def send_data_to_tcp(self, data):
        self.transport.write(data.encode())

    def connection_lost(self, exc):
        msg = 'Connection lost with the server...'
        info = self.transport.get_extra_info('peername')
        # server_udp[1].tcp_client_disconnected(msg, info)


# UDP Server
class UdpServer(asyncio.DatagramProtocol):
    CLIENT_TCP_TIMEOUT = 5.0

    def __init__(self):
        self.client_tcp_timeout = None

    def connection_made(self, transport):
        print('start', transport)
        self.transport = transport
        while True:
            cmd = input("udp:")
            self.send_data_to_udp(cmd)

    def datagram_received(self, data, addr):
        self.data = data.strip().decode()
        print('Data received:', self.data, addr)

        # if self.data == 'send to tcp.':
        #    client_tcp[1].send_data_to_tcp(self.data)

    def connection_lost(self, exc):
        print('stop', exc)

    def send_data_to_udp(self, data):
        print('Send udp data: ', (data))
        self.transport.sendto(data.encode())

    def connect_client_tcp(self):
        pass

    # coro = loop.create_connection(TcpClient, 'localhost', 8000)
    # client_tcp = loop.run_until_complete(coro)
    # client_tcp = asyncio.async(coro)

    def tcp_client_disconnected(self, data, info):
        print(data)
        self.client_tcp_info = info
        self.client_tcp_timeout = asyncio.get_event_loop().call_later(self.CLIENT_TCP_TIMEOUT, self.connect_client_tcp)

    def tcp_client_connected(self):
        if self.client_tcp_timeout:
            self.client_tcp_timeout.cancel()
            print('call_later cancel.')


loop = asyncio.get_event_loop()

# UDP Server
# coro_udp = loop.create_datagram_endpoint(UdpServer, local_addr=('localhost', 5555))
# server_udp = asyncio.Task(coro)
# server_udp = False

# TCP client
coro_tcp = loop.create_connection(TcpClient, 'localhost', 8000)
# client_tcp = asyncio.async(coro)
client_tcp = False


# client_tcp = loop.run_until_complete(coro)


# Main thread
@asyncio.coroutine
async def listener(loop):
    server_udp = False

    while True:
        cmd = input(">>")

        if cmd == 'udp':
            print("Udp started")
            coro = loop.create_datagram_endpoint(UdpServer, remote_addr=('localhost', 5555))
            server_udp = loop.create_task(coro)
            await server_udp


loop.run_until_complete(listener(loop))

try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.close()
    print("Bye bye")
