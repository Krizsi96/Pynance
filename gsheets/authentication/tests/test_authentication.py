import pytest
from unittest.mock import patch, Mock
from authentication.authentication import Authentication


def test_first_log_in_without_credentials():
    # Then
    with pytest.raises(FileNotFoundError):
        # When
        auth = Authentication(path_to_credentials="not_existing_credentials.json")


def test_first_log_in_with_credentials():
    # When
    auth = Authentication(path_to_credentials="some_credentials.json")

    # Then
    assert auth.path_to_credentials == "some_credentials.json"
