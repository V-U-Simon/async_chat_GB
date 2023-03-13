import json
from socket import socket
from time import time


def send_message(s: socket, message: dict):
    encoded_message = json.dumps(message).encode("utf-8")
    s.sendall(encoded_message)


def recv_message(s: socket) -> dict:
    data = s.recv(1024)
    decoded_message = json.loads(data.decode("utf-8"))
    return decoded_message


presence = {
    "action": "presence",
    "time": time(),
    "type": "status",
    "user": {
        "account_name": "C0deMaver1ck",
        "status": "online",
    }
}

presence_check = {
    "action": "probe",
    "time": time(),
}

responce = {
    "response": 200,
    "time": time(),
    # "alert": "message (optional for 2xx codes)",
}
