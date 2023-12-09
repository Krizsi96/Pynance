import pytest
from unittest.mock import patch, Mock
from pathlib import Path
from authentication.authentication import (
    Authentication,
    folder_contains_credentials_file,
    folder_contains_token_file,
    token_is_valid,
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


@patch("authentication.authentication.Path")
def test_folder_contains_credentials_file(mocked_path):
    # When
    folder_contains_credentials_file("/path/to/credentials.json")

    # Then
    mocked_path.assert_called_once_with("/path/to/credentials.json")


@patch("authentication.authentication.Path")
def test_folder_contains_token_file(mocked_path):
    # When
    folder_contains_token_file("/path/to/token.json")

    # Then
    mocked_path.assert_called_once_with("/path/to/token.json")


@pytest.fixture
def auth_fixture():
    with patch(
        "authentication.authentication.folder_contains_credentials_file"
    ) as mocked_folder_contains_credentials_file:
        mocked_folder_contains_credentials_file.return_value = True
        test_auth = Authentication(credentials_folder="/path/to/existing/credentials")
        credentials_folder = Path("/path/to/existing/credentials")
        return test_auth, credentials_folder


def test_check_with_valid_token(auth_fixture):
    # Given
    test_auth = auth_fixture[0]
    token_path = auth_fixture[1].joinpath("token.json")

    with patch(
        "authentication.authentication.folder_contains_token_file"
    ) as mocked_folder_contains_token_file:
        mocked_folder_contains_token_file.return_value = True

        with patch("builtins.print") as mocked_print:
            # when
            return_value = test_auth.check()

    # Then
    mocked_print.assert_called_once_with("Authentication OK")
    mocked_folder_contains_token_file.assert_called_once_with(token_path)
    assert return_value is True


def test_check_with_invalid_token(auth_fixture):
    # Given
    test_auth = auth_fixture[0]
    token_path = auth_fixture[1].joinpath("token.json")

    with patch(
        "authentication.authentication.folder_contains_token_file"
    ) as mocked_folder_contains_token_file:
        mocked_folder_contains_token_file.return_value = True

        with patch(
            "authentication.authentication.token_is_valid"
        ) as mocked_token_is_valid:
            mocked_token_is_valid.return_value = False

            # When
            return_value = test_auth.check()

    # Then
    mocked_folder_contains_token_file.assert_called_once_with(token_path)
    mocked_token_is_valid.assert_called_once_with(token_path)
    assert return_value is False


def test_check_with_not_existing_token(auth_fixture):
    # Given
    test_auth = auth_fixture[0]
    token_path = auth_fixture[1].joinpath("token.json")

    with patch(
        "authentication.authentication.folder_contains_token_file"
    ) as mocked_folder_contains_token_file:
        mocked_folder_contains_token_file.return_value = False

        # When
        return_value = test_auth.check()

    # Then
    mocked_folder_contains_token_file.assert_called_once_with(token_path)
    return_value is False
