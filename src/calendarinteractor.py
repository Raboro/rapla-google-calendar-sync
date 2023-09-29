from event import Event
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError

import os


class CalendarInteractor:
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    TOKEN_FILE_PATH = "token.json"

    def fetch_credentials(self) -> Credentials:
        credentials = None

        if os.path.exists(self.TOKEN_FILE_PATH):
            credentials = Credentials.from_authorized_user_file(self.TOKEN_FILE_PATH)

        if self.__no_credentials(credentials):
            credentials = self.__fetch_credentials(credentials)
            self.__save_to_file(credentials)

        return credentials

    def __no_credentials(self, credentials: Credentials) -> bool:
        return not credentials or not credentials.valid

    def __fetch_credentials(self, credentials: Credentials) -> Credentials:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self.SCOPES)
            credentials = flow.run_local_server(port=0)

        return credentials

    def __save_to_file(self, credentials: Credentials) -> None:
        with open(self.TOKEN_FILE_PATH, "w") as token_file:
            token_file.write(credentials.to_json())

    def build_service(self, credentials: Credentials) -> Resource:
        try:
            return build('calendar', 'v3', credentials=credentials)
        except HttpError as error:
            print(error)
            exit(1)

    def get_calendar_id(self, service: Resource, calendar_name: str) -> str:
        calendars = service.calendarList().list().execute()
        return next((calendar["id"] for calendar in calendars["items"] if calendar["summary"] == calendar_name), None)
 
    def fetch_all_events(self, service: Resource, calendar_id: str) -> None:
        return service.events().list(calendarId=calendar_id).execute().get("items", [])

    def insert_event(self, event: Event, service: Resource, calendar_id: str) -> None:
        service.events().insert(calendarId=calendar_id, body=event.parse()).execute()
