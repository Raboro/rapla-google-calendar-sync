from event import Event
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError

import os

SCOPES = ["https://www.googleapis.com/auth/calendar"]
TOKEN_FILE_PATH = "token.json"

def fetch_credentials() -> Credentials:

    def no_credentials(credentials: Credentials) -> bool:
        return not credentials or not credentials.valid

    def fetch_credentials(credentials: Credentials) -> Credentials:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)

        return credentials

    def save_to_file(credentials: Credentials) -> None: 
        with open(TOKEN_FILE_PATH, "w") as token_file:
            token_file.write(credentials.to_json())

    credentials = None

    if os.path.exists(TOKEN_FILE_PATH):
        credentials = Credentials.from_authorized_user_file(TOKEN_FILE_PATH)

    if no_credentials(credentials):
        credentials = fetch_credentials(credentials)
        save_to_file(credentials)

    return credentials

def build_service(credentials: Credentials) -> Resource:
    try:
        return build('calendar', 'v3', credentials=credentials)
    except HttpError as error:
        print(error)
        exit(1)

def get_calendar_id(service: Resource, calendar_name: str) -> str:
    calendars = service.calendarList().list().execute()
    return next((calendar["id"] for calendar in calendars["items"] if calendar["summary"] == calendar_name), None)

def insert_event(event: Event, service: Resource, calendar_id: str) -> None:
    service.events().insert(calendarId=calendar_id, body=event.parse()).execute()
