from alive_progress import alive_bar
from calendarinteractor import CalendarInteractor
from eventDTO import EventDTO
from icalparser import IcalParser

import os


if __name__ == "__main__":
    ical_parser = IcalParser()
    ical_parser.fetch_data()
    calendar_interactor = CalendarInteractor()
    credentials = calendar_interactor.fetch_credentials()
    service = calendar_interactor.build_service(credentials)
    calendar_id = calendar_interactor.get_calendar_id(service, os.getenv("CALENDAR_NAME"))
    fetched_events: list[EventDTO] = calendar_interactor.fetch_all_events(service, calendar_id)
    counter = 0
    events = ical_parser.construct_events()

    with alive_bar(len(events)) as bar:
        for event in events:
            if event.should_be_inserted(fetched_events):
                calendar_interactor.insert_event(event, service, calendar_id)
                counter += 1
            bar()
    print("\nAdded in total", counter)
    