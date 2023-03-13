from socket import socket, AF_INET, SOCK_STREAM
from conf import DEFAULT_IP, DEFAULT_PORT
from loguru import logger
import argparse


def main():
    parser = argparse.ArgumentParser(description='run server')
    parser.add_argument('--address', '-a', type=str, default=DEFAULT_IP, help='set server address (default: 127.0.0.1)')
    parser.add_argument('--port', '-p', type=int, default=DEFAULT_PORT, help='set server port (default: 8893)')
    args = parser.parse_args()

    run_server(args.address, args.port)


def run_server(address, port):
    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind((address, port))
        logger.debug(f'start server on {address}:{port}')
        s.listen(5)

        while True:
            s_connect, client_address = s.accept()
            logger.debug(f"Client connected from {client_address}")

            try:
                data = s_connect.recv(1024)
                logger.debug(f"Received data: {data}")
                s_connect.send(b"message form server: get your message")
            finally:
                s_connect.close


if __name__ == "__main__":
    main()
