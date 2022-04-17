"""Парсер сайта БГТУ, который позволяет получать расписание и список групп.

Возможности:

• `parse_schedule(group)` - получить список с расписанием для заданной группы.

• `parser_groups(faculty, year)` - получить список групп по заданным факультету и году.
"""

from typing import List

from fastapi import FastAPI, Query
import uvicorn

from bgtu_parser import Parser
from models import Schedule


parser = Parser()
app = FastAPI(title="API БГТУ (Unofficial)",
              docs_url='/', version="v2.0.0",
              description="Данное API даёт возможность получить группы и их расписание с сайта БГТУ. Страница на Github: [xhable1337/bgtu-parser](https://github.com/xhable1337/bgtu-parser)")


@app.get("/api/v2/schedule",
         response_model=Schedule,
         summary="Расписание заданной группы",
         tags=("Методы API",))
def get_schedule(group: str = Query(None, description='Группа, для которой ведётся парсинг расписания', example='О-20-ИВТ-1-по-Б')):
    """Парсит и возвращает расписание для заданной группы на всё полугодие."""
    return parser.schedule(group)


@app.get("/api/v2/groups",
         response_model=List[str],
         summary="Список групп по факультету и году поступления",
         tags=("Методы API",))
def get_schedule(faculty: str = Query(None, description='Факультет, группы которого нужно найти', example='Факультет информационных технологий'),
                 year: str = Query(None, description='Год поступления в университет', example='20')):
    """Парсит и возвращает все группы заданного года поступления на заданном факультете."""
    return parser.groups(faculty, year)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8443)
