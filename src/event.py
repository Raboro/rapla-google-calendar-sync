from dataclasses import dataclass
from datetime import datetime
from dotenv import load_dotenv

import os
import pytz


load_dotenv()


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
        time_zone = os.getenv("TIME_ZONE")
        event = {
            "summary": self.summary,
            "description": self.description,
            "colorId": self.color_id,
            "start": self.__construct_time_element(self.start, time_zone),
            "end": self.__construct_time_element(self.end, time_zone),
            "location": self.location
        }
        if (self.recurrence != ""):
            event["recurrence"] = ["RRULE:" + self.recurrence]
        return event

    def __construct_time_element(self, time: str, time_zone: str) -> dict[str, str]:
        return {
            "dateTime": self.__to_rfc3339(time),
            "timeZone": time_zone
        }

    def __to_rfc3339(self, time: str) -> str:
        if not time.endswith("Z"):
            time += "Z"
        datetime_obj = datetime.strptime(time, "%Y%m%dT%H%M%SZ")
        return datetime_obj.replace(tzinfo=pytz.UTC).isoformat().replace("+00:00", "+02:00")
