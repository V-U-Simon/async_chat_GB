import atexit
from socket import socket as sock
from socket import AF_INET, SOCK_STREAM
from select import select

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
            socket.setblocking(False)
            logger.debug(f'start server on {self.address}:{self.port} with max connections: {MAX_CONNECTIONS}')

            self.inputs: list[sock] = [socket]
            self.outputs: list[sock] = []
            exepts: list[sock] = []
            self.messages = {}

            while True:
                read, send, close = select(self.inputs, self.outputs, self.inputs, 1)
                self.process_read(read, send, close)
                self.process_send(read, send, close)
                self.process_close(read, send, close)

    def process_read(self, read, send, close):
        for connection in read:
            if connection is self.socket:
                # create connection
                client_socket, client_address = self.socket.accept()
                client_socket.setblocking(False)
                self.inputs.append(client_socket)
                logger.debug(f"Client connected from {client_socket}, {client_address}")
            else:
                # read connection
                data = recv_data(connection)
                if data:
                    self.messages.setdefault(connection, []).append(data)
                    if connection not in self.outputs:
                        self.outputs.append(connection)

                    # Responce for valid messages
                    response = Responce200(alert='success message')
                    send_data(client_socket, data=response)
                else:
                    # close the connection
                    close.append(connection)

    def process_send(self, read, send, close):
        for connection in send:
            # todo: here will be implemented sending the message
            # data = messages[connection].pop()
            # send_data(client_socket, data=response)
            self.outputs.remove(connection)

    def process_close(self, read, send, close):
        for connection in close:
            # close the connection
            self.inputs.remove(connection)
            close.remove(connection)
            if connection in self.outputs:
                self.outputs.remove(connection)
            if self.messages.get(connection):
                del self.messages[connection]
            connection.close()
            logger.debug(f"Client connenction is closed {connection}")

    def finally_close_all_connections(self):
        if hasattr(self, 'connection'):
            for connection in self.inputs:
                logger.debug(f"Client connenction is closed {connection}")
                connection.close()


# Register the close_socket function to be called on exit

if __name__ == "__main__":
    server = Server(DEFAULT_IP, DEFAULT_PORT)

    atexit.register(server.finally_close_all_connections)

    server.run()
