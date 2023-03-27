import atexit
from socket import socket as sock
from socket import AF_INET, SOCK_STREAM
from select import select

from messenger.config import DEFAULT_IP, DEFAULT_PORT, MAX_CONNECTIONS
from messenger.protocol.request import AuthQuit
from messenger.utils import send_data, recv_data
from messenger.utils import log, logger
from messenger.protocol import Responce200
from messenger.protocol import Message, AuthPresence, AccountName


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
            self.exepts: list[sock] = []
            self.users: list[AccountName] = []
            self.messages = {}

            while True:
                read_sockets, send_sockets, close_sockets = select(self.inputs, self.outputs, self.inputs, 1)
                self.process_read(read_sockets, send_sockets, close_sockets)
                self.process_send(read_sockets, send_sockets, close_sockets)
                self.process_close(read_sockets, send_sockets, close_sockets)

    def process_read(self, read_sockets, send_sockets, close_sockets):
        for connection in read_sockets:
            if connection is self.socket:
                # create connection
                connection, client_address = self.socket.accept()
                connection.setblocking(False)
                self.inputs.append(connection)
                logger.debug(f"Client connected from {connection}, {client_address}")
            else:
                # read connection
                data = recv_data(connection)
                if data:
                    # authentication
                    if isinstance(data, AuthPresence):
                        user: AccountName = data.user
                        self.users.append(user)

                    if isinstance(data, AuthQuit):
                        user: AccountName = data.user
                        self.users.remove(user)

                    # pass data to output if message
                    if isinstance(data, Message):
                        self.messages.setdefault(connection, []).append(data)
                        if connection not in self.outputs:
                            self.outputs.append(connection)

                    # Responce for valid messages
                    response = Responce200(alert='success message')
                    send_data(connection, data=response)
                else:
                    # close the connection
                    close_sockets.append(connection)

    def process_send(self, read_sockets, send_sockets, close_sockets):
        for connection in send_sockets:

            # Sending a message like echo but uppercasing
            data: Message = self.messages[connection].pop()
            if isinstance(data, Message):
                data.message = data.message.upper()
            send_data(connection, data=data)
            self.outputs.remove(connection)

    def process_close(self, read_sockets, send_sockets, close_sockets):
        for connection in close_sockets:
            # close the connection
            self.inputs.remove(connection)
            close_sockets.remove(connection)
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
