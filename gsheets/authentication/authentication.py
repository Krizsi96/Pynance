from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError

CREDENTIALS_FILE_NAME = "credentials.json"
TOKEN_FILE_NAME = "token.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


class Authentication:
    """Authentication class for Google Sheets API"""

    def __init__(self, credentials_folder):
        self.path_to_credentials = Path(credentials_folder).joinpath(
            CREDENTIALS_FILE_NAME
        )
        self.path_to_token = Path(credentials_folder).joinpath(TOKEN_FILE_NAME)
        self.credentials = None
        self.SCOPES = SCOPES
        if not folder_contains_credentials_file(self.path_to_credentials):
            raise FileNotFoundError("Credentials file not found in the specified folder")

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
        self.credentials = run_with_timeout(flow.run_local_server, timeout=60, port=0)
        if self.credentials:
            return True
        else:
            return False

    def valid_credentials(self):
        """Checks if credentials are valid"""
        if self.credentials and self.credentials.valid:
            return True
        else:
            return False

    def credentials_need_refresh(self):
        """Checks if the credentials are expired and can be refreshed"""
        if (
            self.credentials
            and self.credentials.expired
            and self.credentials.refresh_token
        ):
            return True
        else:
            return False

    def save_credentials(self):
        """Saves credentials if not empty to token.json file for future use"""
        if self.credentials:
            with open(self.path_to_token, "w") as token:
                token.write(self.credentials.to_json())


def folder_contains_credentials_file(path_to_credentials):
    return Path(path_to_credentials).is_file()


def folder_contains_token_file(path_to_token):
    return Path(path_to_token).is_file()


def load_from_token(path_to_token, scopes):
    return Credentials.from_authorized_user_file(path_to_token, scopes)


def run_with_timeout(func, timeout, *args, **kwargs):
    executor = ThreadPoolExecutor(max_workers=1)
    future = executor.submit(func, *args, **kwargs)
    try:
        return future.result(timeout=timeout)
    except FutureTimeoutError:
        print(f"TimeoutError for func: {func.__name__}, timeout: {timeout}")
        return None
    finally:
        executor.shutdown(wait=False)
