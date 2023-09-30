from dataclasses import dataclass
from datetime import datetime
import datetime as dt
from dotenv import load_dotenv

import os
import pytz

from eventDTO import EventDTO


load_dotenv()

TIME_ZONE = os.getenv("TIME_ZONE")

@dataclass(frozen=True)
class Event:
    summary: str
    description: str
    color_id: int
    start: str
    end: str
    location: str
    recurrence: str

    def parse(self) -> dict[str, str | int]:
        event = {
            "summary": self.summary,
            "description": self.description,
            "colorId": self.color_id,
            "start": self.__construct_time_element(self.start),
            "end": self.__construct_time_element(self.end),
            "location": self.location
        }
        if (self.recurrence != ""):
            event["recurrence"] = ["RRULE:" + self.recurrence]
        return event

    def __construct_time_element(self, time: str) -> dict[str, str]:
        return {
            "dateTime": self.__to_rfc3339(time),
            "timeZone": TIME_ZONE
        }

    def __to_rfc3339(self, time: str) -> str:
        if not time.endswith("Z"):
            time += "Z"
        datetime_obj = datetime.strptime(time, "%Y%m%dT%H%M%SZ")
        return datetime_obj.replace(tzinfo=pytz.UTC).isoformat().replace("+00:00", "+02:00")

    def should_be_inserted(self, fetched_events: list[EventDTO]) -> bool:
        return not self.__in_past() and self.__should_be_inserted_not_in_past(fetched_events)
    
    def __in_past(self) -> bool:
        date = datetime.fromisoformat(self.__to_rfc3339(self.end))
        current_date = datetime.now(date.tzinfo)
        return date < current_date
    
    def __should_be_inserted_not_in_past(self, fetched_events: list[EventDTO]) -> bool:
        for fetched_event in fetched_events:
            if self.__equals(fetched_event):
                return False
        return True
    
    def __equals(self, fetched_event: EventDTO) -> bool:
        same_summary = self.summary == fetched_event.summary
        same_start_time = self.__same_time(self.__to_rfc3339(self.start), fetched_event.start.date_time)
        same_end_time = self.__same_time(self.__to_rfc3339(self.end), fetched_event.end.date_time)
        return same_summary and same_start_time and same_end_time and self.__same_recurrence(fetched_event.recurrence)
    
    def __same_time(self, time1: str, time2: str) -> bool:
        return self.__convert_to_utc(time1) == self.__convert_to_utc(time2)

    def __convert_to_utc(self, time: str) -> str:
        try:
            return datetime.fromisoformat(time).astimezone(dt.timezone.utc)
        except ValueError:
            return ""    

    def __same_recurrence(self, recurrence: list[str]) -> bool:
        both_empty = self.recurrence == "" and recurrence == []
        return True if both_empty else self.__same_recurrence_both_not_empty(recurrence)
    
    def __same_recurrence_both_not_empty(self, recurrence: list[str]) -> bool:
        self_empty_and_fetched_not = self.recurrence == "" and recurrence != []
        self_not_but_fetched_empty = self.recurrence != "" and recurrence == [] 
        if self_empty_and_fetched_not or self_not_but_fetched_empty:
            return False
        return ["RRULE:" + self.recurrence] == recurrence