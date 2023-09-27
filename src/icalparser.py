from dotenv import load_dotenv
from event import Event

import os
import icalendar
import urllib3


load_dotenv()


class IcalParser:

   
   def fetch_data(self) -> None:
      self.__save_to_file(self.__fetch_data_of_url())


   def __fetch_data_of_url(self) -> bytes:
      response = urllib3.request("GET", os.getenv("ICAL_URL"))
      if (response.status == 200):
         return response.data
      
      print(f"Invalid status code: {response.status}")
      exit(1)


   def __save_to_file(self, data: bytes) -> None:
      with open("../icalFile.ics", "wb") as ical_file: 
        ical_file.write(data)

   def construct_events(self) -> list[Event]:
      calendar = icalendar.Calendar.from_ical(open("../icalFile.ics", "rb").read())
      events: list[Event] = []
      for event in calendar.walk("VEVENT"):
         if (event.get("RRULE") != None):
            recurrence = event.get("RRULE").to_ical().decode("utf-8")
         else:
            recurrence = ""
         events.append(Event(
            summary=event.get("SUMMARY").to_ical().decode("utf-8"),
            description="" if event.get("DESCRIPTION") == None else event.get("DESCRIPTION").to_ical().decode("utf-8"),
            color_id=6,
            start=event.get("DTSTART").to_ical().decode("utf-8"),
            end=event.get("DTEND").to_ical().decode("utf-8"),
            location=event.get("LOCATION").to_ical().decode("utf-8") ,
            recurrence=recurrence
         ))
      return events
            