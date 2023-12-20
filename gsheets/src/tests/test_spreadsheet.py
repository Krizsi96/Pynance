import pytest
from unittest.mock import patch, MagicMock
from src.spreadsheet import Spreadsheet


@patch("src.spreadsheet.build")
def test_spreadsheet_id_is_stored_during_initialization(mocked_build):
    # Given
    spreadsheet_id = "spreadsheet_id"

    # When
    spreadsheet = Spreadsheet(spreadsheet_id, "credentials")

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


@pytest.fixture
@patch("src.spreadsheet.build")
def spreadsheet_test(mocked_build):
    mocked_service = MagicMock()
    mocked_build.return_value = mocked_service
    credentials = "credentials"
    return Spreadsheet(spreadsheet_id="your_spreadsheet_id", credentials=credentials)


def test_spreadsheet_update(spreadsheet_test):
    # Given
    spreadsheet = spreadsheet_test

    with patch.object(
        spreadsheet.service.spreadsheets().values(), "update"
    ) as mock_update:
        # When
        spreadsheet.update(range="A1", value="Test Value")

        # Then
        mock_update.assert_called_once_with(
            spreadsheetId="your_spreadsheet_id",
            range="A1",
            valueInputOption="USER_ENTERED",
            body={"values": [["Test Value"]]},
        )


@patch("src.spreadsheet.logging")
def test_log_successfull_update(mocked_logging, spreadsheet_test):
    # Given
    spreadsheet = spreadsheet_test

    with patch.object(spreadsheet.service.spreadsheets().values(), "update"):
        # When
        spreadsheet.update(range="A1", value="Test Value")

        # Then
        mocked_logging.info.assert_called_once_with(
            "spreadsheet id#your_spreadsheet_id updated 'A1' with 'Test Value'"
        )
