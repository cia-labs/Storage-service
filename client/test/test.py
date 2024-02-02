import pytest
import requests
from unittest.mock import patch
from clientinterface import save, get




@pytest.fixture
def mock_requests_post():
    with patch("requests.post") as mock_post:
        yield mock_post

def test_save_success(mock_requests_post):
    API_URL = "http://127.0.0.1:8000"
    key = "testkey"
    value = ["encoded_content_1", "encoded_content_2"]

    success_message = {'message': 'File uploaded successfully', 'key': key}
    mock_requests_post.return_value.status_code = 200
    mock_requests_post.return_value.json.return_value = success_message

    response = save(API_URL, key, value)

    assert response.status_code == 200
    assert response.json() == success_message

    mock_requests_post.assert_called_once_with(f"{API_URL}/upload/", data={"key": key, "encoded_content": value})

def test_save_failure(mock_requests_post):
    API_URL = "http://127.0.0.1:8000"
    key = "testkey"
    value = []
    error_message = '{"detail":[{"type":"missing","loc":["body","encoded_content"],"msg":"Field required","input":null,"url":"https://errors.pydantic.dev/2.5/v/missing"}]}'
    mock_requests_post.return_value.status_code = 422  
    mock_requests_post.return_value.text = error_message

    response = save(API_URL, key, value)

    assert response.status_code == 422
    assert response.text == error_message

    mock_requests_post.assert_called_once_with(f"{API_URL}/upload/", data={"key": key, "encoded_content": value})

@pytest.fixture
def mock_requests_get():
    with patch("requests.get") as mock_get:
        yield mock_get

def test_retrieve_success(mock_requests_get):
    API_URL = "http://127.0.0.1:8000"
    key = "test_key"
    value = ["encoded_content_1", "encoded_content_2"]
    save(API_URL, key, value)
    success_response = ["encoded_content_1", "encoded_content_2"]

    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = success_response

    result = get(API_URL, key)

    assert result == success_response

    mock_requests_get.assert_called_once_with(f"{API_URL}/get/{key}")

def test_retrieve_failure(mock_requests_get):
    API_URL = "http://127.0.0.1:8000"
    key = "nonexistent_key"
    error_response = {"detail": "Key not found"}

    mock_requests_get.return_value.status_code = 404
    mock_requests_get.return_value.json.return_value = error_response

    result = get(API_URL, key)
    
    assert result == error_response

    mock_requests_get.assert_called_once_with(f"{API_URL}/get/{key}")
