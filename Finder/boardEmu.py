import socket
import re
import sys
from threading import Thread

print("Searching server...")


def getIP():
    return [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in
            [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]


isServer = False


def startLighthouse():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    message = "board_1\r\n"

    ip = getIP()
    multicast_ip = re.sub("\d+$", "255", ip)
    port = 5555
    data = None

    #sock.setblocking(0)

    sock.sendto(message.encode(), (multicast_ip, port))

    try:
        print("Try to recieve data")
        data = sock.recvfrom(512)
    except socket.error:
        print("No data")
        print(socket.error.strerror)
        '''no data yet..'''

    if data:
        print("Response from server: ", data[0])
        sock.close()
        return data[1]


while True:
    command = input(">>")
    if command == 'exit':
        sys.exit()

    if command == 'udp':
        server = startLighthouse()
        print("Server: ", server)

'''
//Search controller server
Controller findController(IPAddress curIP)
{
    Serial.println("Searching server...");

    bool isServer = false;
    IPAddress multicastIp = IPAddress(curIP[0], curIP[1], curIP[2], 255);
    Controller cntr;
    while (!isServer)
    {
        //Sending broadcast message
        Serial.println("blink lighthouse");

        //send hello world to server
        //data will be sent to server
        char buffer[50] = "board_1";
        Udp.beginPacket(multicastIp, udpPort);
        Udp.write(buffer);
        Udp.endPacket();
        memset(buffer, 0, 50);
        //processing incoming packet, must be called before reading the buffer
        Udp.parsePacket();
        //receive response from server, it will be HELLO WORLD
        if (Udp.read(buffer, 50) > 0)
        {
            Serial.print("Controller found: ");
            Serial.print(Udp.remoteIP());
            Serial.print(":");
            Serial.println(Udp.remotePort());
            cntr.ip = Udp.remoteIP();
            cntr.port = Udp.remotePort();
            isServer = true;
        }
        //Wait for 1 second
        delay(1000);
    }

    return cntr;
}
'''
