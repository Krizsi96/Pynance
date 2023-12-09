import os


class Authentication:
    """
    Authentication class for Google Sheets API
    """

    def __init__(self, path_to_credentials):
        if not os.path.exists(path_to_credentials):
            raise FileNotFoundError
        self.path_to_credentials = path_to_credentials
