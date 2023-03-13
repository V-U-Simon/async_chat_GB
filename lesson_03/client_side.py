from socket import socket, AF_INET, SOCK_STREAM
from vars import server_address
from loguru import logger

with socket(AF_INET, SOCK_STREAM) as s:
    s.connect(server_address)

    s.send(b"test message")
    data = s.recv(1024)
    logger.debug(data.decode("utf-8"))