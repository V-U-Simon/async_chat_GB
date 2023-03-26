# ========================= Аспекты безопасности ==============================

# ------------- Простая аутентификация клиента. Реализация клиента -------------

import os
import hmac
from socket import socket, AF_INET, SOCK_STREAM


def client_authenticate(connection, secret_key):
    """
    Аутентификация клиента на удаленном сервисе.
    Параметр connection - сетевое соединение (сокет)
    secret_key - ключ шифрования, известный клиенту и серверу
    """

    # принимаем случайное послание от сервера
    message = connection.recv(4096)

    # вычисляем HMAC-функцию
    # <hmac.HMAC object at 0x000000BACEF3D278>
    # b'?\xa0\x85\x94`\xb9[\xe8\x865\x97\xb6\x06\x1e\xefj'
    hash = hmac.new(secret_key, message)
    digest = hash.digest()

    # отправляем ответ серверу
    connection.send(digest)


# ------------------------------ Клиент ----------------------------- #

secret_key = b'our_secret_key'

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('localhost', 9999))

# проходим аутентификацию
client_authenticate(sock, secret_key)

sock.send(b'Hello, my secure server!')
resp = sock.recv(4096)

print(f'Сервер ответил: {resp.decode()}')
