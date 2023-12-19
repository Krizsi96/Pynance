import pytest
from unittest.mock import patch
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
