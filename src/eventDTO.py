from dataclasses import dataclass

@dataclass(frozen=True)
class Time:
    date_time: str
    time_zone: str

    def __repr__(self) -> str:
        return f"date_time={self.date_time}, time_zone={self.time_zone}"

@dataclass(frozen=True)
class EventDTO:
    summary: str
    start: Time
    end: Time 
    recurrence: list[str]

    @classmethod
    def from_dict(cls, data: dict):
        if cls.__is_full_day(data):
            start = Time(date_time=data["start"]["date"], time_zone="")
            end = Time(date_time=data["end"]["date"], time_zone="")
        else:
            start = Time(date_time=data["start"]["dateTime"], time_zone=data["start"]["timeZone"])
            end = Time(date_time=data["end"]["dateTime"], time_zone=data["end"]["timeZone"])

        return cls(
            summary=data.get("summary", ""),
            start=start,
            end=end,
            recurrence=data.get("recurrence", []),
        )
    
    @classmethod
    def __is_full_day(cls, data: dict) -> bool:
        try:
            return data["start"]["date"] != None
        except KeyError:
            return False

    def __repr__(self) -> str:
        return f"summary={self.summary} \nstart=[{self.start}] \nend=[{self.end}] \nrecurrence={self.recurrence}"