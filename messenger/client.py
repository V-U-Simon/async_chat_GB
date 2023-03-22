from socket import socket as sock
from socket import AF_INET, SOCK_STREAM

from messenger.config import DEFAULT_IP, DEFAULT_PORT
from messenger.protocol import AuthPresence
from messenger.protocol.request import Request
from messenger.protocol.response import Responce
from messenger.utils import send_data, recv_data
from messenger.utils import log, logger


class Client:

    def __init__(self, ip, port):
        self.address = ip
        self.port = port

    @logger.catch
    def run(self):
        with sock(AF_INET, SOCK_STREAM) as socket:
            # create socket and connect to the server
            self.socket: sock = socket
            self.connect_to_server()
            self.send_presence_report()
            while True:
                message = input('write some test: ')

            # send message
            # todo: send data to server

    @log()
    def connect_to_server(self):
        connect_status: int = self.socket.connect_ex((self.address, self.port))
        if connect_status != 0:
            logger.error(f'🔌🚨 failed to connect to server: {connect_status}')
            exit(1)
        return self.socket.getsockname()

    @log()
    def send_presence_report(self):
        presonce_message: Request = AuthPresence(User=None)  #todo: define user
        send_data(self.socket, presonce_message)

        data: Responce = recv_data(self.socket)
        return data


if __name__ == '__main__':
    client = Client(DEFAULT_IP, DEFAULT_PORT)
    client.run()