from googleapiclient.discovery import build


class Spreadsheet:
    def __init__(self, spreadsheet_id: str, credentials):
        self.spreadsheet_id = spreadsheet_id
        self.service = build("sheets", "v4", credentials=credentials)

    def get(self):
        pass

    def update(self):
        pass
