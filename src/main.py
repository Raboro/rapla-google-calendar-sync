from calendarinteractor import CalendarInteractor
from icalparser import IcalParser

import os


if __name__ == "__main__":
    ical_parser = IcalParser()
    ical_parser.fetch_data()
    calendar_interactor = CalendarInteractor()
    credentials = calendar_interactor.fetch_credentials()
    service = calendar_interactor.build_service(credentials)
    calendar_id = calendar_interactor.get_calendar_id(service, os.getenv("CALENDAR_NAME"))
    for event in ical_parser.construct_events():
        calendar_interactor.insert_event(event, service, calendar_id)