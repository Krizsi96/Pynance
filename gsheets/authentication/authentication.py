from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

CREDENTIALS_FILE_NAME = "credentials.json"
TOKEN_FILE_NAME = "token.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


class Authentication:
    """
    Authentication class for Google Sheets API
    """

    def __init__(self, credentials_folder):
        if not folder_contains_credentials_file(credentials_folder):
            raise FileNotFoundError
        self.path_to_credentials = Path(credentials_folder).joinpath(
            CREDENTIALS_FILE_NAME
        )
        self.path_to_token = Path(credentials_folder).joinpath(TOKEN_FILE_NAME)
        self.credentials = None

    def check(self):
        is_check_ok = False
        if folder_contains_token_file(self.path_to_token):
            self.credentials = load_from_token(self.path_to_token)
            if self.credentials and self.credentials.valid:
                print("Authentication OK")
                is_check_ok = True
            elif (
                self.credentials
                and self.credentials.expired
                and self.credentials.refresh_token
            ):
                self.credentials.refresh(Request())
                print("Authentication Refreshed")
                is_check_ok = True

        return is_check_ok


def folder_contains_credentials_file(path_to_credentials):
    return Path(path_to_credentials).is_file()


def folder_contains_token_file(path_to_token):
    return Path(path_to_token).is_file()


def load_from_token(path_to_token):
    return Credentials.from_authorized_user_file(path_to_token, SCOPES)
