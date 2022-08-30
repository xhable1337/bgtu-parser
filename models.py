"""models.py"""
from datetime import datetime
from typing import List, Union

from pydantic import BaseModel

# pylint: disable=R0903
# Модели не нуждаются в методах

#! Модели для представления расписания студентов


class Lesson(BaseModel):
    """Модель пары.

    #### Поля модели

    - `number` (int): номер пары
    - `subject` (int): предмет
    - `room` (str): аудитория
    - `teacher` (str): преподаватель (-ли)
    """
    number: int
    subject: str
    room: str
    teacher: str


class Weekday(BaseModel):
    """Модель дня недели.

    #### Поля модели

    - `even` (List[Lesson]): нечётная неделя
    - `odd` (List[Lesson]): чётная неделя
    """
    even: List[Lesson]
    odd: List[Lesson]


class Schedule(BaseModel):
    """Модель расписания.

    #### Поля модели

    - `group` (str): группа
    - `last_updated` (datetime): дата и время обновления
    - `monday` (Weekday): расписание на понедельник
    - `tuesday` (Weekday): расписание на вторник
    - `wednesday` (Weekday): расписание на среду
    - `thursday` (Weekday): расписание на четверг
    - `friday` (Weekday): расписание на пятницу
    - `saturday` (Weekday): расписание на субботу
    """
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
    """Модель пары преподавателя.

    #### Поля модели

    - `number` (int): номер пары
    - `subject` (int): предмет
    - `room` (str): аудитория
    - `teacher` (str): преподаватель (-ли)
    """
    number: int
    subject: str
    room: str
    group: str


class TeacherWeekday(BaseModel):
    """Модель дня недели преподавателя.

    #### Поля модели

    - `even` (List[Lesson]): нечётная неделя
    - `odd` (List[Lesson]): чётная неделя
    """
    even: List[TeacherLesson]
    odd: List[TeacherLesson]


class TeacherSchedule(BaseModel):
    """Модель расписания преподавателя.

    #### Поля модели

    - `last_updated` (datetime): дата и время обновления
    - `monday` (Weekday): расписание на понедельник
    - `tuesday` (Weekday): расписание на вторник
    - `wednesday` (Weekday): расписание на среду
    - `thursday` (Weekday): расписание на четверг
    - `friday` (Weekday): расписание на пятницу
    - `saturday` (Weekday): расписание на субботу
    """
    last_updated: datetime
    monday: TeacherWeekday
    tuesday: TeacherWeekday
    wednesday: TeacherWeekday
    thursday: TeacherWeekday
    friday: TeacherWeekday
    saturday: TeacherWeekday


class Teacher(BaseModel):
    """Модель преподавателя.

    #### Поля модели

    - `name` (str): полное ФИО
    - `initials` (str): инициалы
    - `faculty` (str | None): факультет
    - `department` (str | None): кафедра
    - `phone` (str | None): номер телефона
    - `email` (str | None): личный email адрес
    - `img_src` (str | None): ссылка на фото с сайта БГТУ
    - `schedule` (dict): словарь расписания
    """
    name: str
    initials: str
    faculty: Union[str, None]
    department: Union[str, None]
    phone: Union[str, None]
    email: Union[str, None]
    img_src: str
    schedule: dict
