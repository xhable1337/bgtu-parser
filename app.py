"""app.py

Главный запускаемый файл. Представляет собой API endpoint, написанный на FastAPI.
"""

import os
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException, Query

from bgtu_parser import Parser
from models import Schedule, Teacher, TeacherSchedule

# pylint: disable=C0103
# В угоду красивому коду константы останутся в snake-case
abs_file_path = os.path.abspath(__file__)
path, filename = os.path.split(abs_file_path)
parser = Parser(path + '/chromedriver')
description = (
    "Данное API даёт возможность получить группы и их расписание с сайта БГТУ. "
    "Страница на Github: [xhable1337/bgtu-parser](https://github.com/xhable1337/bgtu-parser)"
)
app = FastAPI(title="API БГТУ (Unofficial)",
              docs_url='/', version="v2.0.0",
              description=description)


@app.get("/api/v2/schedule",
         response_model=Schedule,
         summary="Расписание заданной группы",
         tags=("Студенты",))
def get_schedule(group: str = Query(
        default=None,
        description='Группа, для которой ведётся парсинг расписания',
        example='О-20-ИВТ-1-по-Б'
)):
    """Парсит и возвращает расписание для заданной группы на всё полугодие."""
    return parser.schedule(group)


@app.get("/api/v2/groups",
         response_model=List[str],
         summary="Список групп по факультету и году поступления",
         tags=("Студенты",))
def get_groups(
        faculty: str = Query(
            default=None,
            description='Факультет, группы которого нужно найти',
            example='Факультет информационных технологий'
        ),
        year: str = Query(
            default=None,
            description='Год поступления в университет',
            example='20'
        )
):
    """Парсит и возвращает все группы заданного года поступления на заданном факультете."""
    return parser.groups(faculty, year)


@app.get("/api/v2/teacher_list",
         response_model=List[str],
         summary="Список имён преподавателей",
         tags=("Преподаватели",))
def get_teacher_list():
    """Парсит и возвращает список имён всех преподавателей."""
    return parser.teacher_list()


@app.get("/api/v2/teacher_info",
         response_model=Teacher,
         summary="Информация о преподавателе",
         tags=("Преподаватели",))
def get_teacher_info(
        name: str = Query(
            default=None,
            description='Имя преподавателя',
            example='Трубаков Евгений Олегович'
        )
):
    """Парсит и возвращает информацию о заданном преподавателе."""
    return parser.teacher_info(name)


@app.get("/api/v2/teacher",
         response_model=Teacher,
         summary="Преподаватель",
         tags=("Преподаватели",))
def get_teacher(name: str = Query(
        default=None,
        description='Имя преподавателя',
        example='Трубаков Евгений Олегович'
)):
    """Парсит и возвращает преподавателя (информация и расписание)."""
    schedule = parser.teacher_schedule(name)

    if not schedule:
        raise HTTPException(
            status_code=404, detail="У преподавателя нет расписания")

    info = parser.teacher_info(name)
    info['schedule'] = schedule
    return info


@app.get("/api/v2/teacher_schedule",
         response_model=TeacherSchedule,
         summary="Расписание преподавателя",
         tags=("Преподаватели",))
def get_teacher_schedule(
        teacher: str = Query(
            default=None,
            description='Имя преподавателя',
            example='Трубаков Евгений Олегович'
        )
):
    """Парсит и возвращает расписание заданного преподавателя."""
    return parser.teacher_schedule(teacher)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8443)
