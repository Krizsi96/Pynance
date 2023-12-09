import pytest
from unittest.mock import patch, Mock
from authentication.authentication import Authentication


@patch("authentication.authentication.os.path.exists")
def test_start_without_credentials(mocked_path_exists):
    # Given
    mocked_path_exists.return_value = False

    # Then
    with pytest.raises(FileNotFoundError):
        # When
        auth = Authentication(path_to_credentials="not_existing_credentials.json")


@patch("authentication.authentication.os.path.exists")
def test_start_with_credentials(mocked_path_exists):
    # Given
    mocked_path_exists.return_value = True

    # When
    auth = Authentication(path_to_credentials="some_credentials.json")

    # Then
    assert auth.path_to_credentials == "some_credentials.json"
