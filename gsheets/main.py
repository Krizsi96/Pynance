#!/usr/bin/env python3
import os
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def main():
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())

    spreadsheet_id = None
    if os.path.exists("spreadsheet.json"):
        with open("spreadsheet.json", "r") as spreadsheet:
            spreadsheet_id = json.load(spreadsheet)["spreadsheet_id"]
    else:
        print("Please create a spreadsheet.json file")
        exit(1)

    try:
        service = build("sheets", "v4", credentials=credentials)
        sheets = service.spreadsheets()

        for row in range(2, 7):
            number1 = int(
                sheets.values()
                .get(spreadsheetId=spreadsheet_id, range=f"Sheet1!A{row}")
                .execute()
                .get("values")[0][0]
            )
            number2 = int(
                sheets.values()
                .get(spreadsheetId=spreadsheet_id, range=f"Sheet1!B{row}")
                .execute()
                .get("values")[0][0]
            )
            calculation_result = number1 + number2
            print(f"Processing {number1} + {number2} = {calculation_result}")

            sheets.values().update(
                spreadsheetId=spreadsheet_id,
                range=f"Sheet1!C{row}",
                valueInputOption="USER_ENTERED",
                body={"values": [[f"{calculation_result}"]]},
            ).execute()

            sheets.values().update(
                spreadsheetId=spreadsheet_id,
                range=f"Sheet1!D{row}",
                valueInputOption="USER_ENTERED",
                body={"values": [["DONE"]]},
            ).execute()

    except HttpError as error:
        print(error)


if __name__ == "__main__":
    main()
