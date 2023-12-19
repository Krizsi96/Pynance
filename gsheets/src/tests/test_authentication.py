import pytest
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path
from src.authentication import (
    Authentication,
    folder_contains_credentials_file,
    folder_contains_token_file,
)


@patch("src.authentication.folder_contains_credentials_file")
def test_init_with_not_existing_credentials(mocked_folder_contains_credentials_file):
    # Given
    mocked_folder_contains_credentials_file.return_value = False

    # Then
    with pytest.raises(FileNotFoundError):
        # When
        Authentication(credentials_folder="/path/to/not/existing/credentials")

    mocked_folder_contains_credentials_file.assert_called_once_with(
        Path("/path/to/not/existing/credentials/credentials.json")
    )


@patch("src.authentication.folder_contains_credentials_file")
def test_init_with_existing_credentials(mocked_folder_contains_credentials_file):
    # Given
    mocked_folder_contains_credentials_file.return_value = True

    # When
    test_auth = Authentication(credentials_folder="/path/to/existing/credentials")

    # Then
    mocked_folder_contains_credentials_file.assert_called_once_with(
        Path("/path/to/existing/credentials/credentials.json")
    )
    assert (
        str(test_auth.path_to_credentials)
        == "/path/to/existing/credentials/credentials.json"
    )
    assert str(test_auth.path_to_token) == "/path/to/existing/credentials/token.json"


@patch("src.authentication.Path")
def test_folder_contains_credentials_file(mocked_path):
    # When
    folder_contains_credentials_file("/path/to/credentials.json")

    # Then
    mocked_path.assert_called_once_with("/path/to/credentials.json")


@patch("src.authentication.Path")
def test_folder_contains_token_file(mocked_path):
    # When
    folder_contains_token_file("/path/to/token.json")

    # Then
    mocked_path.assert_called_once_with("/path/to/token.json")


@pytest.fixture
def auth_fixture():
    with patch(
        "src.authentication.folder_contains_credentials_file"
    ) as mocked_folder_contains_credentials_file:
        mocked_folder_contains_credentials_file.return_value = True
        test_auth = Authentication(credentials_folder="/path/to/existing/credentials")
        credentials_folder = Path("/path/to/existing/credentials")
        return test_auth, credentials_folder


@pytest.mark.parametrize(
    "expired, refresh_token, valid, expected_message, expected_return_value",
    [
        # expired token without refresh token
        (
            True,
            False,
            False,
            "expired token",
            False,
        ),
        # expired token with refresh token
        (
            True,
            True,
            False,
            "refreshed token",
            True,
        ),
        # valid token
        (False, False, True, "valid token", True),
    ],
)
def test_check_with_different_tokens(
    auth_fixture, expired, refresh_token, valid, expected_message, expected_return_value
):
    # Given
    test_auth = auth_fixture[0]
    token_path = auth_fixture[1].joinpath("token.json")

    with patch("src.authentication.Credentials") as MockCredentials:
        mock_credentials = MagicMock()
        mock_credentials.expired = expired
        mock_credentials.refresh_token = refresh_token
        mock_credentials.valid = valid

        MockCredentials.from_authorized_user_file.return_value = mock_credentials

        with patch(
            "src.authentication.folder_contains_token_file"
        ) as mocked_folder_contains_token_file:
            mocked_folder_contains_token_file.return_value = True

            with patch("src.authentication.logging") as mocked_logging:
                # when
                return_value = test_auth.check_credentials()

    # Then
    mocked_logging.info.assert_called_once_with(expected_message)
    mocked_folder_contains_token_file.assert_called_once_with(token_path)
    assert return_value is expected_return_value


def test_check_with_not_existing_token(auth_fixture):
    # Given
    test_auth = auth_fixture[0]
    token_path = auth_fixture[1].joinpath("token.json")

    with patch(
        "src.authentication.folder_contains_token_file"
    ) as mocked_folder_contains_token_file:
        mocked_folder_contains_token_file.return_value = False

        # When
        return_value = test_auth.load_credentials()

    # Then
    mocked_folder_contains_token_file.assert_called_once_with(token_path)
    assert return_value is False


def test_successful_login(auth_fixture):
    # Given
    test_auth = auth_fixture[0]

    with patch("src.authentication.InstalledAppFlow") as MockedInstalledAppFlow:
        mocked_flow = MagicMock()
        mocked_flow.run_local_server.return_value = MagicMock()
        MockedInstalledAppFlow.from_client_secrets_file.return_value = mocked_flow

        # When
        return_value = test_auth.login()

    # Then
    assert return_value is True
    mocked_flow.run_local_server.assert_called_once()
    MockedInstalledAppFlow.from_client_secrets_file.assert_called_once_with(
        test_auth.path_to_credentials, test_auth.SCOPES
    )


def test_login_timeout(auth_fixture):
    # Given
    test_auth = auth_fixture[0]

    with patch("src.authentication.InstalledAppFlow") as MockedInstalledAppFlow:
        mocked_flow = MagicMock()
        mocked_flow.run_local_server.return_value = None
        MockedInstalledAppFlow.from_client_secrets_file.return_value = mocked_flow

        with patch("src.authentication.run_with_timeout") as mocked_run_with_timeout:
            mocked_run_with_timeout.return_value = None

            # When
            return_value = test_auth.login()

    # Then
    assert return_value is False
    mocked_run_with_timeout.assert_called_once_with(
        mocked_flow.run_local_server, timeout=60, port=0
    )
    MockedInstalledAppFlow.from_client_secrets_file.assert_called_once_with(
        test_auth.path_to_credentials, test_auth.SCOPES
    )


def test_saving_of_credentials(auth_fixture):
    # Given
    test_auth = auth_fixture[0]

    mock_credentials = MagicMock()
    mock_credentials.expired = False
    mock_credentials.refresh_token = False
    mock_credentials.valid = True

    test_auth.credentials = mock_credentials

    with patch("src.authentication.open", mock_open()) as mocked_open:
        # When
        test_auth.save_credentials()

    # Then
    mocked_open.assert_called_once_with(test_auth.path_to_token, "w")
    mocked_open().write.assert_called_once_with(test_auth.credentials.to_json())


def test_saving_of_empty_credentials(auth_fixture):
    # Given
    test_auth = auth_fixture[0]
    with patch("src.authentication.open", mock_open()) as mocked_open:
        # When
        test_auth.save_credentials()

    # Then
    mocked_open.assert_not_called()
    mocked_open().write.assert_not_called()