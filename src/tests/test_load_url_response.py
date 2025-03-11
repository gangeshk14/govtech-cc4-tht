import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils')))
import pytest
import requests
import requests_mock
from load_url_response import load_json_url_response  

def test_load_json_url_response_success():
    """
    Test successful JSON retrieval from a URL.
    """
    url = "https://example.com/data.json"
    mock_data = {"key": "value"}

    with requests_mock.Mocker() as m:
        m.get(url, json=mock_data)
        result = load_json_url_response(url)
        assert result == mock_data

def test_load_json_url_response_http_error():
    """
    Test handling of HTTP errors (e.g., 404 Not Found).
    """
    url = "https://example.com/invalid.json"

    with requests_mock.Mocker() as m:
        m.get(url, status_code=404)
        result = load_json_url_response(url)
        assert result is None

def test_load_json_url_response_invalid_json():
    """
    Test handling of invalid JSON responses.
    """
    url = "https://example.com/invalid.json"

    with requests_mock.Mocker() as m:
        m.get(url, text="invalid json")
        result = load_json_url_response(url)
        assert result is None

def test_load_json_url_response_connection_error():
    """
    Test handling of connection errors (e.g., network issues).
    """
    url = "https://example.com/data.json"

    with requests_mock.Mocker() as m:
        m.get(url, exc=requests.exceptions.ConnectionError)
        result = load_json_url_response(url)
        assert result is None

def test_load_json_url_response_unexpected_error():
    """
    Test handling of unexpected errors.
    """
    url = "https://example.com/data.json"

    with requests_mock.Mocker() as m:
        m.get(url, exc=Exception("Unexpected error"))
        result = load_json_url_response(url)
        assert result is None