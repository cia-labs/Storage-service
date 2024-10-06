# test_client.py

import pytest
import requests
from unittest.mock import patch
from client import save, get, update_data, update_key, append, delete_key

# Fixtures to mock requests methods
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

# Test cases for the 'save' function
def test_save_success(mock_requests_post):
    API_URL = "http://127.0.0.1:8080"
    key = "testkey"
    data_list = [b"data1", b"data2"]

    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = b"Data uploaded successfully: key = testkey"

    mock_requests_post.return_value = mock_response

    response = save(API_URL, key, data_list)

    assert response.status_code == 200
    assert response.text == "Data uploaded successfully: key = testkey"

    expected_url = f"{API_URL}/upload/{key}"
    expected_headers = {'Content-Type': 'application/octet-stream'}
    mock_requests_post.assert_called_once()
    called_args, called_kwargs = mock_requests_post.call_args
    assert called_args[0] == expected_url
    assert 'data' in called_kwargs
    assert 'headers' in called_kwargs
    assert called_kwargs['headers'] == expected_headers

def test_save_failure_key_exists(mock_requests_post):
    API_URL = "http://127.0.0.1:8080"
    key = "existingkey"
    data_list = [b"data1", b"data2"]

    mock_response = requests.Response()
    mock_response.status_code = 400
    mock_response._content = b"Key already exists"

    mock_requests_post.return_value = mock_response

    response = save(API_URL, key, data_list)

    assert response.status_code == 400
    assert response.text == "Key already exists"

# Test cases for the 'get' function
def test_get_success(mock_requests_get):
    API_URL = "http://127.0.0.1:8080"
    key = "testkey"

    # Mock the parse_flatbuffer function
    with patch('client.parse_flatbuffer') as mock_parse_flatbuffer:
        mock_parse_flatbuffer.return_value = [b"data1", b"data2"]

        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = b"flatbufferdata"  # Placeholder binary data

        mock_requests_get.return_value = mock_response

        result = get(API_URL, key)

        assert result == [b"data1", b"data2"]

        expected_url = f"{API_URL}/get/{key}"
        mock_requests_get.assert_called_once_with(expected_url)

def test_get_failure_not_found(mock_requests_get, capsys):
    API_URL = "http://127.0.0.1:8080"
    key = "nonexistentkey"

    mock_response = requests.Response()
    mock_response.status_code = 404
    mock_response._content = b"No data found for key: nonexistentkey"

    mock_requests_get.return_value = mock_response

    result = get(API_URL, key)

    assert result is None  # The get function returns None on failure
    assert "Error during retrieval" in capsys.readouterr().out

# Test cases for the 'update_data' function
def test_update_data_success(mock_requests_post):
    API_URL = "http://127.0.0.1:8080"
    key = "testkey"
    data_list = [b"newdata1", b"newdata2"]

    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = b"Data uploaded successfully: key = testkey"

    mock_requests_post.return_value = mock_response

    response = update_data(API_URL, key, data_list)

    assert response.status_code == 200
    assert response.text == "Data uploaded successfully: key = testkey"

    expected_url = f"{API_URL}/update_data/{key}"
    expected_headers = {'Content-Type': 'application/octet-stream'}
    mock_requests_post.assert_called_once()
    called_args, called_kwargs = mock_requests_post.call_args
    assert called_args[0] == expected_url
    assert 'data' in called_kwargs
    assert 'headers' in called_kwargs
    assert called_kwargs['headers'] == expected_headers

def test_update_data_failure(mock_requests_post):
    API_URL = "http://127.0.0.1:8080"
    key = "nonexistentkey"
    data_list = [b"newdata1", b"newdata2"]

    mock_response = requests.Response()
    mock_response.status_code = 404
    mock_response._content = b"Key not found: nonexistentkey"

    mock_requests_post.return_value = mock_response

    response = update_data(API_URL, key, data_list)

    assert response.status_code == 404
    assert response.text == "Key not found: nonexistentkey"

# Test cases for the 'update_key' function
def test_update_key_success(mock_requests_put):
    API_URL = "http://127.0.0.1:8080"
    old_key = "oldkey"
    new_key = "newkey"

    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = b"Key updated successfully from oldkey to newkey"

    mock_requests_put.return_value = mock_response

    response_text = update_key(API_URL, old_key, new_key)

    assert response_text == "Key updated successfully from oldkey to newkey"

    expected_url = f"{API_URL}/update/{old_key}/{new_key}"
    mock_requests_put.assert_called_once_with(expected_url)

def test_update_key_failure(mock_requests_put):
    API_URL = "http://127.0.0.1:8080"
    old_key = "nonexistentkey"
    new_key = "newkey"

    mock_response = requests.Response()
    mock_response.status_code = 404
    mock_response._content = b"Key not found: nonexistentkey"

    mock_requests_put.return_value = mock_response

    response_text = update_key(API_URL, old_key, new_key)

    assert response_text == "Key not found: nonexistentkey"

# Test cases for the 'append' function
def test_append_success(mock_requests_post):
    API_URL = "http://127.0.0.1:8080"
    key = "testkey"
    data_list = [b"appenddata1", b"appenddata2"]

    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = b"Data appended successfully: key = testkey"

    mock_requests_post.return_value = mock_response

    response_text = append(API_URL, key, data_list)

    assert response_text == "Data appended successfully: key = testkey"

    expected_url = f"{API_URL}/append/{key}"
    expected_headers = {'Content-Type': 'application/octet-stream'}
    mock_requests_post.assert_called_once()
    called_args, called_kwargs = mock_requests_post.call_args
    assert called_args[0] == expected_url
    assert 'data' in called_kwargs
    assert 'headers' in called_kwargs
    assert called_kwargs['headers'] == expected_headers

def test_append_failure(mock_requests_post):
    API_URL = "http://127.0.0.1:8080"
    key = "nonexistentkey"
    data_list = [b"appenddata1", b"appenddata2"]

    mock_response = requests.Response()
    mock_response.status_code = 404
    mock_response._content = b"No data found for key: nonexistentkey"

    mock_requests_post.return_value = mock_response

    response_text = append(API_URL, key, data_list)

    assert response_text == "No data found for key: nonexistentkey"

# Test cases for the 'delete_key' function
def test_delete_key_success(mock_requests_delete):
    API_URL = "http://127.0.0.1:8080"
    key = "testkey"

    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = b"File deleted successfully: key = testkey"

    mock_requests_delete.return_value = mock_response

    response_text = delete_key(API_URL, key)

    assert response_text == "File deleted successfully: key = testkey"

    expected_url = f"{API_URL}/delete/{key}"
    mock_requests_delete.assert_called_once_with(expected_url)

def test_delete_key_failure(mock_requests_delete):
    API_URL = "http://127.0.0.1:8080"
    key = "nonexistentkey"

    mock_response = requests.Response()
    mock_response.status_code = 404
    mock_response._content = b"Key not found"

    mock_requests_delete.return_value = mock_response

    response_text = delete_key(API_URL, key)

    assert response_text == "Key not found"

# Additional test cases for edge conditions and exceptions
def test_save_exception(mock_requests_post):
    API_URL = "http://127.0.0.1:8080"
    key = "testkey"
    data_list = [b"data1", b"data2"]

    mock_requests_post.side_effect = requests.RequestException("Network error")

    response = save(API_URL, key, data_list)

    assert response is None

def test_get_exception(mock_requests_get):
    API_URL = "http://127.0.0.1:8080"
    key = "testkey"

    mock_requests_get.side_effect = requests.RequestException("Network error")

    result = get(API_URL, key)

    assert result is None

