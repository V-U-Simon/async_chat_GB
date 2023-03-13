from socket import socket, AF_INET, SOCK_STREAM
from conf import DEFAULT_IP, DEFAULT_PORT
from loguru import logger

with socket(AF_INET, SOCK_STREAM) as s:
    s.connect((DEFAULT_IP, DEFAULT_PORT))

    s.send(b"test message")
    data = s.recv(1024)
    logger.debug(data.decode("utf-8"))
