from dataclasses import dataclass
from dotenv import load_dotenv

import os

load_dotenv()

@dataclass(frozen=True)
class Event():
    summary: str
    description: str
    color_id: int 
    start: str 
    end: str

    def parse(self) -> dict[str, str | int]:
        return {
            "summary": self.summary,
            "description": self.description,
            "colorId": self.color_id,
            "start": {
                "dateTime": self.start,
                "timeZone": os.getenv("TINE_ZONE")
            },
            "end": {
                "dateTime": self.end,
                "timeZone": os.getenv("TINE_ZONE")
            }
        } 
