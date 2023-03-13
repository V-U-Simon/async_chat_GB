import json
from socket import socket, AF_INET, SOCK_STREAM
from time import time
from conf import DEFAULT_IP, DEFAULT_PORT
from loguru import logger
import argparse


# @logger.catch()
def main():
    parser = argparse.ArgumentParser(description='run server')
    parser.add_argument('--address', '-a', type=str, default=DEFAULT_IP, help='set server address (default: 127.0.0.1)')
    parser.add_argument('--port', '-p', type=int, default=DEFAULT_PORT, help='set server port (default: 8893)')
    args = parser.parse_args()

    server = Server(address=args.address, port=args.port)
    server.run()


class Server:

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.max_connections = 5

        # todo: tmp place for error response (replace)
        self.res_200 = {"response": 200, "time": time()}
        self.res_400 = {"response": 400, "time": time()}

    def run(self):
        with socket(AF_INET, SOCK_STREAM) as s:

            self.socket: socket = s
            s.bind((self.address, self.port))
            s.listen(self.max_connections)
            logger.debug(f'🚀 start server on {self.address}:{self.port} with max connections: {self.max_connections}')

            while True:
                self.client_socket, self.client_address = self.socket.accept()
                logger.debug(f"🔌 Client connected from {self.client_socket}")

                try:
                    data = self.get_message()
                    # todo: here will be handle of data
                finally:
                    self.client_socket.close()

    def get_message(self):
        data = self.client_socket.recv(1024)
        decoded_message = json.loads(data.decode("utf-8"))
        logger.info(f'📩 get from server: {data}')

        if self.validated_message(decoded_message):
            self.sent_response(self.res_200)
        else:
            self.sent_response(self.res_400)

        return decoded_message

    @staticmethod
    def validated_message(message: dict):
        check_action: bool = message.get('action') in ['presence', 'probe', 'msg', 'quit', 'authenticate', 'join', 'leave']
        check_time: bool = bool(message.get('time'))
        logger.debug(f'Checking {check_time=} & {check_action=}')
        return check_action and check_time

    def sent_response(self, responce):
        encoded_responce = json.dumps(responce).encode("utf-8")
        self.client_socket.sendall(encoded_responce)
        logger.info(f'📩  send to server: {encoded_responce}')


if __name__ == "__main__":
    main()
