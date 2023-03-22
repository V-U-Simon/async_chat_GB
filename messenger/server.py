from socket import socket as sock
from socket import AF_INET, SOCK_STREAM

from messenger.config import DEFAULT_IP, DEFAULT_PORT, MAX_CONNECTIONS
from messenger.utils import send_data, recv_data
from messenger.utils import log, logger
from messenger.protocol import Responce200


class Server:

    def __init__(self, ip, port):
        self.address = ip
        self.port = port

    @logger.catch
    def run(self):
        with sock(AF_INET, SOCK_STREAM) as socket:

            # create server socket
            self.socket: sock = socket
            socket.bind((self.address, self.port))
            socket.listen(MAX_CONNECTIONS)
            logger.debug(f'start server on {self.address}:{self.port} with max connections: {MAX_CONNECTIONS}')

            while True:

                try:
                    # accept client
                    client_socket, client_address = socket.accept()
                    logger.debug(f"Client connected from {client_socket}, {client_address}")

                    data = recv_data(client_socket)

                    response = Responce200(alert='success message')
                    send_data(client_socket, data=response)

                finally:
                    client_socket.close()


if __name__ == "__main__":
    servet = Server(DEFAULT_IP, DEFAULT_PORT)
    servet.run()
