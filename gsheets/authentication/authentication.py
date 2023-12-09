from pathlib import Path

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

    def check(self):
        is_check_ok = False
        if folder_contains_token_file(self.path_to_token):
            print("Authentication OK")
            is_check_ok = True

        return is_check_ok


def folder_contains_credentials_file(credentials_folder):
    return Path(credentials_folder).joinpath(CREDENTIALS_FILE_NAME).is_file()


def folder_contains_token_file(credentials_folder):
    return Path(credentials_folder).joinpath(TOKEN_FILE_NAME).is_file()
