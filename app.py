"""Парсер сайта БГТУ, который позволяет получать расписание и список групп.

Возможности:

• `parse_schedule(group)` - получить список с расписанием для заданной группы.

• `parser_groups(faculty, year)` - получить список групп по заданным факультету и году.
"""

from typing import List

from fastapi import FastAPI, Query, HTTPException
import os
import uvicorn

from bgtu_parser import Parser
from models import Schedule, Teacher, TeacherSchedule

absFilePath = os.path.abspath(__file__)
path, filename = os.path.split(absFilePath)
parser = Parser(path + '/chromedriver')
app = FastAPI(title="API БГТУ (Unofficial)",
              docs_url='/', version="v2.0.0",
              description="Данное API даёт возможность получить группы и их расписание с сайта БГТУ. Страница на Github: [xhable1337/bgtu-parser](https://github.com/xhable1337/bgtu-parser)")


@app.get("/api/v2/schedule",
         response_model=Schedule,
         summary="Расписание заданной группы",
         tags=("Методы API",))
def get_schedule(group: str = Query(None, description='Группа, для которой ведётся парсинг расписания', example='О-20-ИВТ-1-по-Б')):
    """Парсит и возвращает расписание для заданной группы на всё полугодие."""
    return parser.schedule_v2(group)


@app.get("/api/v2/groups",
         response_model=List[str],
         summary="Список групп по факультету и году поступления",
         tags=("Методы API",))
def get_groups(faculty: str = Query(None, description='Факультет, группы которого нужно найти', example='Факультет информационных технологий'),
               year: str = Query(None, description='Год поступления в университет', example='20')):
    """Парсит и возвращает все группы заданного года поступления на заданном факультете."""
    return parser.groups(faculty, year)


@app.get("/api/v2/teacher_list",
         response_model=List[str],
         summary="Список имён преподавателей",
         tags=("Методы API",))
def get_teacher_list():
    """Парсит и возвращает список имён всех преподавателей."""
    return parser.teacher_list_v2()


@app.get("/api/v2/teacher_info",
         response_model=Teacher,
         summary="Информация о преподавателе",
         tags=("Методы API",))
def get_teacher_info(name: str = Query(None, description='Имя преподавателя', example='Трубаков Евгений Олегович')):
    """Парсит и возвращает информацию о заданном преподавателе."""
    return parser.teacher_info_v2(name)


@app.get("/api/v2/teacher",
         response_model=Teacher,
         summary="Преподаватель",
         tags=("Методы API",))
def get_teacher(name: str = Query(None, description='Имя преподавателя', example='Трубаков Евгений Олегович')):
    """Парсит и возвращает преподавателя (информация и расписание)."""
    schedule = parser.teacher_schedule_v2(name)

    if not schedule:
        raise HTTPException(
            status_code=404, detail="У преподавателя нет расписания")

    info = parser.teacher_info_v2(name)
    info['schedule'] = schedule
    return info


@app.get("/api/v2/teacher_schedule",
         response_model=TeacherSchedule,
         summary="Расписание преподавателя",
         tags=("Методы API",))
def get_teacher_schedule(teacher: str = Query(None, description='Имя преподавателя', example='Трубаков Евгений Олегович')):
    """Парсит и возвращает расписание заданного преподавателя."""
    return parser.teacher_schedule_v2(teacher)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8443)
