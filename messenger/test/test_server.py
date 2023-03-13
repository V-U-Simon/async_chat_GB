import json
import pytest
from socket import socket, AF_INET, SOCK_STREAM
# from messenger.server_side import Server, main
# from messenger.conf import DEFAULT_IP, DEFAULT_PORT

from server_side import *
from conf import DEFAULT_IP, DEFAULT_PORT
from unittest.mock import Mock, patch


@pytest.fixture
def server():
    return Server(address=DEFAULT_IP, port=DEFAULT_PORT)


@pytest.fixture
def client_socket():
    return Mock()


def test_server_validated_message(server):
    message = {"action": "presence", "time": "2022-01-01 12:00:00"}
    assert server.validated_message(message) is True


def test_server_invalidated_message(server):
    message = {"action": "invalid_action", "time": "2022-01-01 12:00:00"}
    assert server.validated_message(message) is False


@patch("socket.socket")
def test_server_run(mock_socket, server, client_socket):
    mock_socket.return_value = client_socket
    message = {"action": "presence", "time": "2022-01-01 12:00:00"}
    client_socket.recv.return_value = json.dumps(message).encode("utf-8")
    server.get_message = Mock(return_value=message)
    server.sent_response = Mock()

    server.run()

    assert mock_socket.called_once_with(AF_INET, SOCK_STREAM)
    assert client_socket.bind.called_once_with((DEFAULT_IP, DEFAULT_PORT))
    assert client_socket.listen.called_once_with(server.max_connections)
    assert client_socket.accept.called_once()
    assert server.get_message.called_once()
    assert server.sent_response.called_once_with(server.res_200)


@pytest.fixture
def mock_args():
    return Mock(address=DEFAULT_IP, port=DEFAULT_PORT)


@patch("argparse.ArgumentParser.parse_args")
@patch("messenger.server.Server.run")
def test_main(mock_run, mock_args):
    mock_args.return_value = mock_args
    main()
    assert mock_args.called_once()
    assert mock_run.called_once()
