from socket import socket, AF_INET, SOCK_STREAM
from conf import DEFAULT_IP, DEFAULT_PORT
from loguru import logger
import argparse


def main():
    parser = argparse.ArgumentParser(description='run client')
    parser.add_argument('--address', '-a', type=str, default=DEFAULT_IP, help='sent to server address (default: 127.0.0.1)')
    parser.add_argument('--port', '-p', type=str, default=DEFAULT_PORT, help='set to server port (default: 8893)')
    args = parser.parse_args()

    run_client(args.address, args.port)


def run_client(address, port):
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((DEFAULT_IP, DEFAULT_PORT))
        logger.debug(f'connected to server ({DEFAULT_IP}:{DEFAULT_PORT})')

        s.send(b"test message")
        data = s.recv(1024)
        logger.debug(data.decode("utf-8"))


if __name__ == '__main__':
    main()