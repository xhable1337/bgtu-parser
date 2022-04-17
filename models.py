from pydantic import BaseModel
from typing import List
from datetime import datetime


class Lesson(BaseModel):
    number: int
    subject: str
    room: str
    teacher: str


class Weekday(BaseModel):
    even: List[Lesson]
    odd: List[Lesson]


class Schedule(BaseModel):
    group: str
    last_updated: datetime
    monday: Weekday
    tuesday: Weekday
    wednesday: Weekday
    thursday: Weekday
    friday: Weekday
