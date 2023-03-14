import json
from socket import socket, AF_INET, SOCK_STREAM
from time import time
from conf import DEFAULT_IP, DEFAULT_PORT
from loguru import logger
import argparse


# @logger.catch
def main():
    parser = argparse.ArgumentParser(description='run client')
    parser.add_argument('--address', '-a', type=str, default=DEFAULT_IP, help='sent to server address (default: 127.0.0.1)')
    parser.add_argument('--port', '-p', type=int, default=DEFAULT_PORT, help='set to server port (default: 8893)')
    args = parser.parse_args()

    client = Client(args.address, args.port)
    client.run()


class Client:

    def __init__(self, address, port):

        self.address = address
        self.port = port

    def run(self):
        with socket(AF_INET, SOCK_STREAM) as s:

            self.socket: socket = s
            logger.debug(f'🆕 created socket: ({self.socket.getsockname()})')

            self.connect_to_server()
            self.presence_report()

    def connect_to_server(self):
        connect_status = self.socket.connect_ex((self.address, self.port))

        if connect_status == 0:
            logger.debug(f'🔌 connected to server ({DEFAULT_IP}:{DEFAULT_PORT})')
        else:
            logger.error(f'🚨 failed to connect to server: {connect_status}')
            exit(1)

    def presence_report(self):
        presence = {
            "action": "presence",
            "time": time(),
            "type": "status",
            "user": {
                "account_name": "C0deMaver1ck",
                "status": "online",
            }
        }

        self.send_message(presence)
        logger.debug(f'presence report sended')
        # data = self.get_response()

    def send_message(self, message):
        encoded_message = json.dumps(message).encode("utf-8")
        self.socket.sendall(encoded_message)
        logger.info(f'📩  send to server: {message}')

    def get_response(self):
        data = self.socket.recv(1024)
        decoded_message = json.loads(data.decode("utf-8"))
        logger.info(f'📩 get from server: {data}')
        return decoded_message


if __name__ == '__main__':
    main()