from socket import socket, AF_INET, SOCK_STREAM
from vars import server_address
from loguru import logger

with socket(AF_INET, SOCK_STREAM) as s:
    s.bind(server_address)
    s.listen(5)

    while True:
        s_connect, client_address = s.accept()
        logger.debug(f"Client connected from {client_address}")

        try:
            data = s_connect.recv(1024)
            logger.debug(f"Received data: {data}")
            s_connect.send(b"message form server: get your message")
        finally:
            s_connect.close()
