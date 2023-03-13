from socket import socket, AF_INET, SOCK_STREAM
from vars import server_address
from loguru import logger


s = socket(AF_INET, SOCK_STREAM)
s.connect(server_address)

s.send(b"test message")
data = s.recv(1024)
logger.debug(data.decode("utf-8"))

s.close()
