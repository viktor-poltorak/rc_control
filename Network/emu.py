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