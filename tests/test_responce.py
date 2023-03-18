import pytest
from messenger.protocol import response
from messenger import utils


@pytest.fixture
def success_respose() -> response.Responce:
    from time import time

    return response.Responce200(
        time=time(),
        alert='success message',
    )


def test_success_response(success_respose):
    assert success_respose.response == 200
    assert success_respose.time != None
    assert isinstance(success_respose.time, float)
    assert success_respose.alert == 'success message'


def test_wrong_success_response(success_respose):
    pass


def test_serialize_success_response(success_respose):

    data_encoded = utils.serialize_data(success_respose)
    assert isinstance(data_encoded, bytes)

    data_parsed: response.Responce200 = utils.deserialize_data(data_encoded)
    assert isinstance(data_parsed, response.Responce)
    assert data_parsed.response == 200
    assert data_parsed.alert == 'success message'


def test_wrong_serialize_success_response(success_respose):
    pass


if __name__ == '__main__':
    pytest.main([__file__, '-s'])
