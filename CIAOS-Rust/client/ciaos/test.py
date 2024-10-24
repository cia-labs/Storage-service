import pytest
import requests
from unittest.mock import patch, Mock
from client import Ciaos

@pytest.fixture
def mock_requests_post():
    with patch('requests.post') as mock_post:
        yield mock_post

@pytest.fixture
def mock_requests_get():
    with patch('requests.get') as mock_get:
        yield mock_get

@pytest.fixture
def mock_requests_put():
    with patch('requests.put') as mock_put:
        yield mock_put

@pytest.fixture
def mock_requests_delete():
    with patch('requests.delete') as mock_delete:
        yield mock_delete

@pytest.fixture
def ciaos_client():
    return Ciaos("testuser")

def test_put_success(mock_requests_post, ciaos_client):
    key = "testkey"
    data_list = [b"data1", b"data2"]

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "Data uploaded successfully: key = testkey"
    mock_requests_post.return_value = mock_response

    response = ciaos_client.put(key, data_list)

    assert response.status_code == 200
    assert response.text == "Data uploaded successfully: key = testkey"

    expected_headers = {'User': "testuser"}
    mock_requests_post.assert_called_once()
    called_args, called_kwargs = mock_requests_post.call_args
    assert "/put/testkey" in called_args[0]
    assert called_kwargs['headers'] == expected_headers

def test_get_success(mock_requests_get, ciaos_client):
    key = "testkey"

    with patch('client.parse_flatbuffer') as mock_parse_flatbuffer:
        mock_parse_flatbuffer.return_value = [b"data1", b"data2"]
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"flatbufferdata"
        mock_requests_get.return_value = mock_response

        result = ciaos_client.get(key)

        assert result == [b"data1", b"data2"]
        expected_headers = {'User': "testuser"}
        mock_requests_get.assert_called_once()
        called_args, called_kwargs = mock_requests_get.call_args
        assert "/get/testkey" in called_args[0]
        assert called_kwargs['headers'] == expected_headers

def test_update_key_success(mock_requests_put, ciaos_client):
    old_key = "oldkey"
    new_key = "newkey"

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "Key updated successfully"
    mock_requests_put.return_value = mock_response

    response_text = ciaos_client.update_key(old_key, new_key)

    assert response_text == "Key updated successfully"
    expected_headers = {'User': "testuser"}
    mock_requests_put.assert_called_once()
    called_args, called_kwargs = mock_requests_put.call_args
    assert "/update_key/oldkey/newkey" in called_args[0]
    assert called_kwargs['headers'] == expected_headers

def test_update_success(mock_requests_post, ciaos_client):
    key = "testkey"
    data_list = [b"newdata1", b"newdata2"]

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "Data updated successfully"
    mock_requests_post.return_value = mock_response

    response = ciaos_client.update(key, data_list)

    assert response.status_code == 200
    assert response.text == "Data updated successfully"
    expected_headers = {'User': "testuser"}
    mock_requests_post.assert_called_once()
    called_args, called_kwargs = mock_requests_post.call_args
    assert "/update/testkey" in called_args[0]
    assert called_kwargs['headers'] == expected_headers

def test_append_success(mock_requests_post, ciaos_client):
    key = "testkey"
    data_list = [b"appenddata1", b"appenddata2"]

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "Data appended successfully"
    mock_requests_post.return_value = mock_response

    response_text = ciaos_client.append(key, data_list)

    assert response_text == "Data appended successfully"
    expected_headers = {'User': "testuser"}
    mock_requests_post.assert_called_once()
    called_args, called_kwargs = mock_requests_post.call_args
    assert "/append/testkey" in called_args[0]
    assert called_kwargs['headers'] == expected_headers

def test_delete_success(mock_requests_delete, ciaos_client):
    key = "testkey"

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "Deleted successfully"
    mock_requests_delete.return_value = mock_response

    response_text = ciaos_client.delete(key)

    assert response_text == "Deleted successfully"
    expected_headers = {'User': "testuser"}
    mock_requests_delete.assert_called_once()
    called_args, called_kwargs = mock_requests_delete.call_args
    assert "/delete/testkey" in called_args[0]
    assert called_kwargs['headers'] == expected_headers