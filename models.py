from pydantic import BaseModel
from typing import List, Optional, Union
from datetime import datetime

#! Модели для представления расписания студентов


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
    saturday: Weekday

#! Модели для представления расписания преподавателей


class TeacherLesson(BaseModel):
    number: int
    subject: str
    room: str
    group: str


class TeacherWeekday(BaseModel):
    even: List[TeacherLesson]
    odd: List[TeacherLesson]


class TeacherSchedule(BaseModel):
    last_updated: datetime
    monday: TeacherWeekday
    tuesday: TeacherWeekday
    wednesday: TeacherWeekday
    thursday: TeacherWeekday
    friday: TeacherWeekday
    saturday: TeacherWeekday


class Teacher(BaseModel):
    name: str
    initials: str
    faculty: Union[str, None]
    department: Union[str, None]
    phone: Union[str, None]
    email: Union[str, None]
    img_src: str
    schedule: dict
