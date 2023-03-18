from socket import socket as sock
from loguru import logger
from pydantic import parse_raw_as
from messenger.config import ENCODING

from messenger.protocol import POSSIBLE_REQUESTS, POSSIBLE_RESPONSES
from messenger.protocol import Responce, Request


def send_data(socket: sock, data: Request | Responce) -> None:
    logger.debug(f'📩  try to send')
    data_encoded = serialize_data(data)
    socket.sendall(data_encoded)
    logger.debug(f'📩  send: {data_encoded}')


def recv_data(socket: sock) -> Request | Responce:
    logger.debug(f'📩 try to receive')
    byte_data: bytes = socket.recv(1024)
    data_parsed = deserialize_data(byte_data)
    logger.debug(f'📩 receive: {data_parsed}')
    return data_parsed


def serialize_data(data: Request | Request):
    logger.debug(f'💾🔀 try to serialize')
    data_json = data.json()
    data_encoded = data_json.encode(ENCODING)
    logger.debug(f'💾🔀 serialize from {type(data)} to {type(data_encoded)}')
    return data_encoded


def deserialize_data(data_encoded: bytes):

    logger.debug(f'💾🔀 try to deserialize')
    data_raw: str = data_encoded.decode(ENCODING)

    simple_data = definite_data(data_raw)

    if isinstance(simple_data, Request):
        type_of_data = simple_data.action
        type_of_data = POSSIBLE_REQUESTS[type_of_data]

    elif isinstance(simple_data, Responce):
        type_of_data = simple_data.response
        type_of_data = POSSIBLE_RESPONSES[type_of_data]

    else:
        logger.error('Unknown type response or request')

    # get treated response
    data_parsed = type_of_data.parse_raw(data_raw)
    logger.debug(f'💾🔀 deserialize from {type(data_encoded)} to {type(data_parsed)}')

    return data_parsed


def definite_data(data_raw: str) -> Request | Responce:
    logger.debug(f"📦🔍 Try to definite data type")

    POSSIBLE_MODELS = [Responce, Request]

    for model in POSSIBLE_MODELS:
        try:
            # parsed_data = parse_raw_as(List[model], raw_bytes)
            parsed_data = parse_raw_as(model, data_raw)
            logger.debug(f"📦🔍 Definite data type: {type(parsed_data)} {parsed_data}")
            return parsed_data
        except ValueError:
            pass
    logger.error(f"📦🔍 Can't define data type for: {data_raw}")
