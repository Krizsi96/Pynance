from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


class Spreadsheet:
    def __init__(self, spreadsheet_id: str, credentials: Credentials):
        self.spreadsheet_id = spreadsheet_id
        self.service = build("sheets", "v4", credentials=credentials)

    def get(self):
        pass

    def update(self, range: str, value):
        self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=range,
            valueInputOption="USER_ENTERED",
            body={"values": [[value]]},
        ).execute()
