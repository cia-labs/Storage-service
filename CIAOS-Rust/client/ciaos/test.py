import pytest
import requests
from unittest.mock import patch
from client import put, get, update, update_key, append, delete

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

def test_put_success(mock_requests_post):
    user = "testuser"
    api_url = "http://127.0.0.1:8080"
    key = "testkey"
    data_list = [b"data1", b"data2"]

    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = b"Data uploaded successfully: key = testkey"
    mock_requests_post.return_value = mock_response

    response = put(user, api_url, key, data_list)

    assert response.status_code == 200
    assert response.text == "Data uploaded successfully: key = testkey"

    expected_url = f"{api_url}/put/{key}"
    expected_headers = {'User': user}
    mock_requests_post.assert_called_once()
    called_args, called_kwargs = mock_requests_post.call_args
    assert called_args[0] == expected_url
    assert called_kwargs['headers'] == expected_headers

def test_get_success(mock_requests_get):
    user = "testuser"
    api_url = "http://127.0.0.1:8080"
    key = "testkey"

    with patch('client.parse_flatbuffer') as mock_parse_flatbuffer:
        mock_parse_flatbuffer.return_value = [b"data1", b"data2"]
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = b"flatbufferdata"
        mock_requests_get.return_value = mock_response

        result = get(user, api_url, key)

        assert result == [b"data1", b"data2"]
        expected_url = f"{api_url}/get/{key}"
        expected_headers = {'User': user}
        mock_requests_get.assert_called_once_with(expected_url, headers=expected_headers)

def test_update_key_success(mock_requests_put):
    user = "testuser"
    api_url = "http://127.0.0.1:8080"
    old_key = "oldkey"
    new_key = "newkey"

    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = b"Key updated successfully"
    mock_requests_put.return_value = mock_response

    response_text = update_key(user, api_url, old_key, new_key)

    assert response_text == "Key updated successfully"
    expected_url = f"{api_url}/update_key/{old_key}/{new_key}"
    expected_headers = {'User': user}
    mock_requests_put.assert_called_once_with(expected_url, headers=expected_headers)

def test_update_success(mock_requests_post):
    user = "testuser"
    api_url = "http://127.0.0.1:8080"
    key = "testkey"
    data_list = [b"newdata1", b"newdata2"]

    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = b"Data updated successfully"
    mock_requests_post.return_value = mock_response

    response = update(user, api_url, key, data_list)

    assert response.status_code == 200
    assert response.text == "Data updated successfully"
    expected_url = f"{api_url}/update/{key}"
    expected_headers = {'User': user}
    mock_requests_post.assert_called_once()
    called_args, called_kwargs = mock_requests_post.call_args
    assert called_args[0] == expected_url
    assert called_kwargs['headers'] == expected_headers

def test_append_success(mock_requests_post):
    user = "testuser"
    api_url = "http://127.0.0.1:8080"
    key = "testkey"
    data_list = [b"appenddata1", b"appenddata2"]

    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = b"Data appended successfully"
    mock_requests_post.return_value = mock_response

    response_text = append(user, api_url, key, data_list)

    assert response_text == "Data appended successfully"
    expected_url = f"{api_url}/append/{key}"
    expected_headers = {'User': user}
    mock_requests_post.assert_called_once()
    called_args, called_kwargs = mock_requests_post.call_args
    assert called_args[0] == expected_url
    assert called_kwargs['headers'] == expected_headers

def test_delete_success(mock_requests_delete):
    user = "testuser"
    api_url = "http://127.0.0.1:8080"
    key = "testkey"

    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = b"Deleted successfully"
    mock_requests_delete.return_value = mock_response

    response_text = delete(user, api_url, key)

    assert response_text == "Deleted successfully"
    expected_url = f"{api_url}/delete/{key}"
    expected_headers = {'User': user}
    mock_requests_delete.assert_called_once_with(expected_url, headers=expected_headers)
