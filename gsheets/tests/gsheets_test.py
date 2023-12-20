from gsheets.gsheets import configure_logging
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
