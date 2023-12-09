import pytest
from unittest.mock import patch, Mock
from authentication.authentication import (
    Authentication,
    folder_contains_credentials_file,
)


@patch("authentication.authentication.folder_contains_credentials_file")
def test_init_with_not_existing_credentials(mocked_folder_contains_credentials_file):
    # Given
    mocked_folder_contains_credentials_file.return_value = False

    # Then
    with pytest.raises(FileNotFoundError):
        # When
        Authentication(credentials_folder="/path/to/not/existing/credentials")

    mocked_folder_contains_credentials_file.assert_called_once_with(
        "/path/to/not/existing/credentials"
    )


@patch("authentication.authentication.folder_contains_credentials_file")
def test_init_with_existing_credentials(mocked_folder_contains_credentials_file):
    # Given
    mocked_folder_contains_credentials_file.return_value = True

    # When
    test_auth = Authentication(credentials_folder="/path/to/existing/credentials")

    # Then
    mocked_folder_contains_credentials_file.assert_called_once_with(
        "/path/to/existing/credentials"
    )
    assert (
        str(test_auth.path_to_credentials)
        == "/path/to/existing/credentials/credentials.json"
    )
    assert str(test_auth.path_to_token) == "/path/to/existing/credentials/token.json"


def test_check_with_valid_token():
    # Given
    with patch(
        "authentication.authentication.folder_contains_credentials_file"
    ) as mocked_folder_contains_credentials_file:
        mocked_folder_contains_credentials_file.return_value = True
        test_auth = Authentication(credentials_folder="/path/to/existing/credentials")

    with patch("builtins.print") as mocked_print:
        # when
        test_auth.check()

    # Then
    mocked_print.assert_called_once_with("Authentication OK")


@patch("authentication.authentication.folder_contains_token_file")
def test_check_with_not_existing_token(mocked_folder_contains_token_file):
    # Given
    with patch(
        "authentication.authentication.folder_contains_credentials_file"
    ) as mocked_folder_contains_credentials_file:
        mocked_folder_contains_credentials_file.return_value = True
        test_auth = Authentication(credentials_folder="/path/to/existing/credentials")
        test_auth.path_to_token = Mock(is_file=Mock(return_value=False))

    mocked_folder_contains_token_file.return_value = False

    # When
    test_auth.check()

    mocked_folder_contains_token_file.assert_called_once_with(
        "/path/to/existing/credentials/token.json"
    )
