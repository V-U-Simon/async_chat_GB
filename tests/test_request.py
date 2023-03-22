from pprint import pprint
from loguru import logger
import pytest

from messenger import protocol
from messenger import utils
from messenger.protocol import request


@pytest.fixture
def user_without_password() -> protocol.UserWithoutPassword:
    user = {"account_name": "C0deMaver1ck", "status": "online"}
    return protocol.UserWithoutPassword(**user)


@pytest.fixture
def message_presence(user_without_password) -> protocol.Request:
    return request.AuthPresence(user=user_without_password)


def test_request_message_presence(message_presence, user_without_password):

    logger.debug(message_presence)
    assert message_presence.action == 'presence'
    assert message_presence.type == 'status'
    assert message_presence.time != None
    assert isinstance(message_presence.time, float)
    assert message_presence.user.account_name == user_without_password.account_name
    assert message_presence.user.status == user_without_password.status


def test_wrong_request_message_presence(message_presence, user_without_password):
    pass


@logger.catch
def test_serialize_request_message_presence(message_presence):

    data_encoded = utils.serialize_data(message_presence)
    assert isinstance(data_encoded, bytes)

    data_parsed: protocol.AuthPresence = utils.deserialize_data(data_encoded)
    assert isinstance(data_parsed, request.Request)
    assert message_presence.action == 'presence'
    assert message_presence.type == 'status'
    assert message_presence.time != None
    assert isinstance(message_presence.time, float)


def test_wrong_serialize_request_message_presence(message_presence):
    pass


if __name__ == '__main__':
    pytest.main([__file__, '-s'])