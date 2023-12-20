from gsheets.gsheets import configure_logging, create_client
from unittest.mock import patch
import pytest
import logging


@patch("gsheets.gsheets.logging.basicConfig")
def test_logging_configuration(mocked_logging_basicConfig):
    # When
    configure_logging()

    # Then
    assert mocked_logging_basicConfig.called_once_with(
        format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG
    )


@patch("gsheets.gsheets.gspread.service_account")
def test_client_creation(mocked_service_account):
    # Given
    filename = "filename"
    mocked_service_account.return_value = "new_client"

    # When
    return_value = create_client(filename)

    # Then
    assert mocked_service_account.called_once_with(filename)
    assert return_value == "new_client"


def test_exception_handling():
    # Given
    filename = "not_existing_file"

    # When
    with pytest.raises(FileNotFoundError, match=f"{filename} not found"):
        create_client(filename)
