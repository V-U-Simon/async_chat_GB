import json
from socket import socket, AF_INET, SOCK_STREAM
from conf import DEFAULT_IP, DEFAULT_PORT
from loguru import logger
import argparse
import time
from utils import send_message, recv_message, presence


@logger.catch
def main():
    parser = argparse.ArgumentParser(description='run client')
    parser.add_argument('--address', '-a', type=str, default=DEFAULT_IP, help='sent to server address (default: 127.0.0.1)')
    parser.add_argument('--port', '-p', type=int, default=DEFAULT_PORT, help='set to server port (default: 8893)')
    args = parser.parse_args()

    run_client(args.address, args.port)


def run_client(address, port):
    with socket(AF_INET, SOCK_STREAM) as s:
        connect_to_server(s, address, port)
        data = recv_message(s)
        logger.info(f'message from server: {data}')


def connect_to_server(s: socket, address, port):

    result = s.connect_ex((address, port))
    if result == 0:
        logger.debug(f'connected to server ({DEFAULT_IP}:{DEFAULT_PORT})')
        logger.debug(f'client: ({s.getsockname()})')
        send_message(s, presence)

    else:
        logger.error(f'failed to connect to server: {result}')
        exit(1)


if __name__ == '__main__':
    main()