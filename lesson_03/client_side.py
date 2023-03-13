from socket import socket, AF_INET, SOCK_STREAM
from vars import server_address

s = socket(AF_INET, SOCK_STREAM)
s.connect(server_address)

s.send(b"test message")
data = s.recv(1024)
print(data.de("utf-8"))

s.close()
