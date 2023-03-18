from messenger import client
from messenger import server
import pytest


@pytest.mark.skip
def test_server_cli():
    server.main()
    # shouldn't return not 0 on success and working work for while


@pytest.mark.skip
def test_client_cli():
    client.main()
    # should return 0 on success