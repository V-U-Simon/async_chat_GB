import pytest
from socket import socket, AF_INET, SOCK_STREAM
from unittest.mock import patch
from ..client_side import Client
from ..conf import DEFAULT_IP, DEFAULT_PORT


@pytest.fixture(scope="module")
def server_socket():
    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind((DEFAULT_IP, DEFAULT_PORT))
        s.listen(1)
        yield s


@pytest.fixture(scope="module")
def client():
    return Client(DEFAULT_IP, DEFAULT_PORT)


@pytest.mark.parametrize("message, expected_response", [({
    "action": "presence",
    "time": 1234567890.123456,
    "type": "status",
    "user": {
        "account_name": "test_user",
        "status": "online"
    }
}, {
    "response": 200,
    "time": 1234567890.123456
}),
                                                        ({
                                                            "action": "invalid_action",
                                                            "time": 1234567890.123456,
                                                            "type": "status",
                                                            "user": {
                                                                "account_name": "test_user",
                                                                "status": "online"
                                                            }
                                                        }, {
                                                            "response": 400,
                                                            "time": 1234567890.123456
                                                        })])
def test_send_and_receive_message(client: Client, server_socket: socket, message: dict[str, str | float | dict[str, str]],
                                  expected_response: dict[str, int | float]):
    # Arrange
    server_conn, server_address = server_socket.accept()

    with patch("messenger.client.socket", return_value=server_conn):
        # Act
        client.run()
        client.send_message(message)
        response = client.get_response()

        # Assert
        assert response == expected_response
