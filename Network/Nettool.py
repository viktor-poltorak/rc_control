import socket


def get_ip():
    '''
    Return current IP address
    :return:string
    '''
    return [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in
            [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
