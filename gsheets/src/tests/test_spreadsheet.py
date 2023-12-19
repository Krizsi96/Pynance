import pytest
from unittest.mock import patch, MagicMock
from src.spreadsheet import Spreadsheet


@patch("src.spreadsheet.build")
def test_spreadsheet_id_is_stored_initialization(mocked_build):
    # Given
    spreadsheet_id = "spreadsheet_id"
    credentials = "credentials"

    # When
    spreadsheet = Spreadsheet(spreadsheet_id, credentials)

    # Then
    assert spreadsheet.spreadsheet_id == spreadsheet_id


@patch("src.spreadsheet.build")
def test_spreadsheet_service_is_created_during_initialization(mocked_build):
    # Given
    mocked_service = MagicMock()
    mocked_build.return_value = mocked_service
    credentials = "credentials"

    # When
    spreadsheet = Spreadsheet("spreadsheet_id", credentials)

    # Then
    mocked_build.assert_called_once_with("sheets", "v4", credentials=credentials)
    assert spreadsheet.service == mocked_service
