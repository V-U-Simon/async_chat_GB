from socket import socket as sock
from socket import AF_INET, SOCK_STREAM
from time import sleep
import threading

from messenger.config import DEFAULT_IP, DEFAULT_PORT
from messenger.protocol import AuthPresence
from messenger.protocol import Request, Responce, Message
from messenger.protocol.request import AuthQuit
from messenger.utils import send_data, recv_data
from messenger.utils import log, logger


class Client:

    def __init__(self, ip, port):
        self.address = ip
        self.port = port

    def recive_messages(self):
        while True:
            data = recv_data(self.socket)
            print(f'--------------------{data}')

    @logger.catch
    def run(self):
        with sock(AF_INET, SOCK_STREAM) as socket:
            # create socket and connect to the server
            self.socket: sock = socket
            self.user = input('введите ваше имя пользователя: ')
            self.connect_to_server()
            self.send_presence_report()

            receive_thread = threading.Thread(target=self.recive_messages)
            receive_thread.start()

            while True:
                self.to = input('введите имя получателя ("exit" для выхода): ')
                if self.to == 'exit':
                    quit_message = AuthQuit(user=self.user)
                    send_data(self.socket, quit_message)
                    sleep(1)

                    self.socket.close()
                    break

                self.message = input('введите сообщение: ')

                message = Message(
                    from_=self.user,
                    to=self.to,
                    message=self.message,
                )

                send_data(self.socket, message)
                # responce = recv_data(self.socket)
                # logger.critical(responce)s

    @log()
    def connect_to_server(self):
        connect_status: int = self.socket.connect_ex((self.address, self.port))
        if connect_status != 0:
            logger.error(f'🔌🚨 failed to connect to server: {connect_status}')
            exit(1)
        return self.socket.getsockname()

    @log()
    def send_presence_report(self):
        presonce_message: Request = AuthPresence(user=self.user)  #todo: define user
        send_data(self.socket, presonce_message)

        data: Responce = recv_data(self.socket)
        return data


if __name__ == '__main__':
    client = Client(DEFAULT_IP, DEFAULT_PORT)
    client.run()