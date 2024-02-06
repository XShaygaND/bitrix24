import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def send_to_sheets(full_name: str, phone_number: str, comment: str):
    """Sends a request to the GoogleAPI to append the data to the sheets"""
    
    sheet_id = os.getenv('GOOGLE_SHEET_ID')

    values = [
        [
            full_name,
            phone_number,
            comment,
        ]
    ]

    return append_values(sheet_id, 'A:C', 'RAW', values)

def append_values(spreadsheet_id, range_name, value_input_option, values):
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    try:
        service = build("sheets", "v4", credentials=creds)
        
        body = {"values": values}
        (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body,
            )
            .execute()
        )

        return (True, None)
    
    except HttpError as error:
        return (False, error)
