from calendarinteractor import fetch_credentials, build_service, get_calendar_id
from icalparser import IcalParser

import os

if __name__ == "__main__":
    ical_parser = IcalParser()
    ical_parser.fetch_data()
    credentials = fetch_credentials()
    service = build_service(credentials)
    calendar_id = get_calendar_id(service, os.getenv("CALENDAR_NAME"))
