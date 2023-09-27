from dataclasses import dataclass
from datetime import datetime
from dotenv import load_dotenv

import os
import pytz


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
