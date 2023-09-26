from dotenv import load_dotenv
from calendarinteractor import fetch_credentials, build_service, get_calendar_id, load

import os
import urllib3

load_dotenv()

def load_data() -> None:
    save_data(fetch_data())

def fetch_data() -> bytes:
    response = urllib3.request("GET", os.getenv("ICAL_URL"))
    if (response.status == 200):
        return response.data
    
    print(f"Invalid status code: {response.status}")
    exit(1)

def save_data(data: bytes) -> None:
    with open("../icalFile.ics", "wb") as ical_file: 
        ical_file.write(data)

if __name__ == "__main__":
    load_data()
    credentials = fetch_credentials()
    service = build_service(credentials)
    calendar_id = get_calendar_id(service, os.getenv("CALENDAR_NAME"))
