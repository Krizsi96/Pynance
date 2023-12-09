from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

CREDENTIALS_FILE_NAME = "credentials.json"
TOKEN_FILE_NAME = "token.json"


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
        self.SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    def check_credentials(self):
        """Checks the credentials and refreshes them if needed

        Returns:
        True - credentials are valid
        False - credentials are invalid
        """
        is_credentials_ok = False
        message = "no token found"
        if self.load_credentials():
            if self.valid_credentials():
                message = "valid token"
                is_credentials_ok = True
            elif self.credentials_need_refresh():
                self.credentials.refresh(Request())
                message = "refreshed token"
                is_credentials_ok = True
            else:
                message = "expired token"
        print(message)
        return is_credentials_ok

    def load_credentials(self):
        """If the token file exists, loads the credentials from it

        Returns:
        True - credentials loaded
        False - can't load credentials
        """
        if folder_contains_token_file(self.path_to_token):
            self.credentials = load_from_token(self.path_to_token, self.SCOPES)
            return True
        else:
            return False

    def login(self):
        """Logs in to Google Sheets API

        Returns:
        True - login successful
        False - login failed
        """
        flow = InstalledAppFlow.from_client_secrets_file(
            self.path_to_credentials, self.SCOPES
        )
        self.credentials = flow.run_local_server(port=0)
        if self.credentials:
            with open(self.path_to_token, "w") as token:
                token.write(self.credentials.to_json())
            return True
        else:
            return False

    def valid_credentials(self):
        return self.credentials and self.credentials.valid

    def credentials_need_refresh(self):
        return (
            self.credentials
            and self.credentials.expired
            and self.credentials.refresh_token
        )


def folder_contains_credentials_file(path_to_credentials):
    return Path(path_to_credentials).is_file()


def folder_contains_token_file(path_to_token):
    return Path(path_to_token).is_file()


def load_from_token(path_to_token, scopes):
    return Credentials.from_authorized_user_file(path_to_token, scopes)
