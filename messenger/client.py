from socket import socket as sock
from socket import AF_INET, SOCK_STREAM
from loguru import logger

from messenger.config import DEFAULT_IP, DEFAULT_PORT
from messenger.protocol import AuthPresence
from messenger.utils import send_data, recv_data


class Client:

    def __init__(self, ip, port):
        self.address = ip
        self.port = port

    @logger.catch
    def run(self):
        with sock(AF_INET, SOCK_STREAM) as socket:

            # create socket and connect to the server
            self.connect_to_server(socket)
            logger.debug(f'🆕 created socket: {socket.getsockname()} and connected to the server')

            # send message
            # todo: send data to server

    def connect_to_server(self, socket: sock):
        logger.debug(f'🔌 try to connected to server')

        # connect to the server
        connect_status = socket.connect_ex((self.address, self.port))
        if connect_status != 0:
            logger.error(f'🔌🚨 failed to connect to server: {connect_status}')
            exit(1)
        logger.debug(f'🔌 connected to server ({DEFAULT_IP}:{DEFAULT_PORT})')

        # send presence message
        logger.debug(f'🔌📩 try to send & receive presence report')
        presonce_message = AuthPresence(User=None)  #todo: define user
        send_data(socket, presonce_message)
        data = recv_data(socket)
        logger.debug(f'🔌📩 send & receive presence report: {data}')


if __name__ == '__main__':
    client = Client(DEFAULT_IP, DEFAULT_PORT)
    client.run()