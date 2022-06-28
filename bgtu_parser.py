from datetime import datetime
import re
import time

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from copy import deepcopy
import requests
import asyncio

from bs4 import BeautifulSoup, Tag
from bs4 import PageElement
from rss_parser import Parser as RSSParser


class Parser:
    def __init__(self,
                 chromedriver_path: str = 'chromedriver.exe',
                 headless: bool = True) -> None:
        self.url = 'https://www.tu-bryansk.ru/education/schedule'
        self.base_url = 'https://www.tu-bryansk.ru'

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTM"
            "L, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.20"
            "6 (Edition Yx GX)"
        )

        if headless:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-browser-side-navigation')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument("--window-size=1920,1080")

        self.driver = webdriver.Chrome(
            executable_path=chromedriver_path,
            chrome_options=chrome_options
        )

        self.driver.implicitly_wait(10)

    def get_initials(self, name: str):
        ln, fn, pn = name.split(' ')
        return f"{ln} {fn[0]}. {pn[0]}."

    def teacher_list_v2(self):
        params = {'form': 'teacher'}
        page = requests.get(self.url, params)
        soup = BeautifulSoup(page.text, 'html.parser')
        combobox = soup.find('select', {'id': 'teacher'})
        options = combobox.find_all('option')
        options = [option.text.replace('_', ' ') for option in options][1:]
        return options

    def teacher_list(self):
        period = '2021-2022_2_1'

        self.driver.get(
            self.url + f'?period={period}&form=teacher')

        time.sleep(0.5)

        teacher_combobox = Select(
            self.driver.find_element_by_xpath('//*[@id="teacher"]'))

        teachers = [option.text for option in teacher_combobox.options]

        return teachers[1:]

    def teacher_schedule_v2(self, teacher: str):
        if not teacher:
            return None
        no = '-'

        days = {'Понедельник': 'monday', 'Вторник': 'tuesday', 'Среда': 'wednesday',
                'Четверг': 'thursday', 'Пятница': 'friday', 'Суббота': 'saturday'}

        lesson_times = {
            '08:00 - 09:35': 1,
            '09:45 - 11:20': 2,
            '11:30 - 13:05': 3,
            '13:20 - 14:55': 4,
            '13:20 - 16:40': 4,
            '15:05 - 16:40': 5,
            '16:50 - 18:25': 6,
            '18:40 - 20:15': 7,
            '18:40 - 20:25': 7,
            '20:25 - 22:00': 8
        }

        teacher_weekday_model_ = {
            'even': [
                {
                    'number': i,
                    'subject': no,
                    'room': no,
                    'group': no
                }
                for i in range(1, 9)
            ],
            'odd': [
                {
                    'number': i,
                    'subject': no,
                    'room': no,
                    'group': no
                }
                for i in range(1, 9)
            ],
        }

        schedule = {
            'last_updated': datetime.now(),
            'monday': deepcopy(teacher_weekday_model_),
            'tuesday': deepcopy(teacher_weekday_model_),
            'wednesday': deepcopy(teacher_weekday_model_),
            'thursday': deepcopy(teacher_weekday_model_),
            'friday': deepcopy(teacher_weekday_model_),
            'saturday': deepcopy(teacher_weekday_model_),
        }

        params = {
            'namedata': 'schedule',
            'teacher': teacher.replace(" ", "_"),
            'period': '2021-2022_2_1',
            'form': 'teacher'
        }
        page = requests.get(self.url + '/schedule.ajax.php', params)
        soup = BeautifulSoup(page.text, 'html.parser')
        rows = soup.find_all('tr')

        row: Tag

        # Тип недели
        week_type = 'both'

        # Время пары
        time = ''

        for row in rows:
            #! День недели
            if row.select_one('.daeweek'):
                day = days[row.text]
                continue

            #! Время
            time_cell = row.select_one('.schtime')

            if not time_cell:
                # ? Времени нет => вторая пара в разделе
                week_type = 'even'

            elif time_cell.has_attr('rowspan'):
                # ? Есть rowspan => первая пара в разделе
                time = time_cell.text.lstrip()
                index = lesson_times[time] - 1
                week_type = 'odd'

            else:
                # ? Есть время, нет rowspan => обычная пара
                time = time_cell.text.lstrip()
                index = lesson_times[time] - 1
                week_type = 'both'

            #! Предмет
            subject_cell = row.select_one('.schname')

            if not subject_cell.text:
                # ? Пары нет (окно)
                continue

            subject_name = subject_cell.contents[0].text
            subject_type = subject_cell.contents[2].text

            if subject_type == 'практическое занятие':
                subject = f"[ПЗ] {subject_name}"

            elif subject_type == 'лекция':
                subject = f"[Л] {subject_name}"

            elif subject_type == 'лабораторное занятие':
                subject = f"[ЛАБ] {subject_name}"

            print(subject)

            #! Группа
            group_cell = row.select_one('.schteacher')
            print(group_cell.text)
            print(group_cell.text.split('.'))

            group = ', '.join([group.strip()
                               for group in group_cell.text.split('.')][:-1])

            #! Аудитория
            room_cell = row.select_one('.schclass')
            room = room_cell.text

            # if splitted

            #! Добавление данных в результирующий словарь
            if week_type == 'both':
                schedule[day]['odd'][index]['number'] = index + 1
                schedule[day]['odd'][index]['subject'] = subject
                schedule[day]['odd'][index]['room'] = room
                schedule[day]['odd'][index]['group'] = group

                schedule[day]['even'][index]['number'] = index + 1
                schedule[day]['even'][index]['subject'] = subject
                schedule[day]['even'][index]['room'] = room
                schedule[day]['even'][index]['group'] = group
            else:
                schedule[day][week_type][index]['number'] = index + 1
                schedule[day][week_type][index]['subject'] = subject
                schedule[day][week_type][index]['room'] = room
                schedule[day][week_type][index]['group'] = group

        return schedule

    def teacher_info_v2(self, name: str):
        teacher = {
            'name': name,
            'initials': self.get_initials(name),
            'faculty': None,
            'department': None,
            'phone': None,
            'email': None,
            'img_src': None,
            'schedule': {}
        }

        url = f'{self.base_url}/sveden/employees/'
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        teacher_card = soup.find('div', {'class': 'fio'}, string=name)

        # ? Если не найдено имя на странице
        if not teacher_card:
            teacher['img_src'] = 'https://www.tu-bryansk.ru/local/templates/bstu/img/nophoto.svg'
            return teacher

        teacher_card = teacher_card.parent.parent.parent

        faculty_field = teacher_card.select_one('div.department-parent.field')
        department_field = teacher_card.select_one('div.department.field')
        phone_field = teacher_card.select_one('div.phone.field')
        email_field = teacher_card.select_one('div.email.field')
        img_field = teacher_card.get('data-photo', None)

        if faculty_field and department_field:
            #! Факультет
            teacher['faculty'] = faculty_field.select_one('.val').text

            #! Кафедра
            teacher['department'] = department_field.select_one('.val').text

            #! Телефон
            if phone_field:
                teacher['phone'] = phone_field.select_one('.val').text

            #! E-mail
            if email_field:
                teacher['email'] = email_field.select_one('.val').text

            #! Фото
            if img_field:
                teacher['img_src'] = str(self.base_url + str(img_field))
            else:
                teacher['img_src'] = 'https://www.tu-bryansk.ru/local/templates/bstu/img/nophoto.svg'

        return teacher

    def groups(self, faculty: str = 'Факультет информационных технологий', year: str = '20'):
        """Получает список групп по заданному факультету с сайта БГТУ, и выводит как результат функции.

        На входе:

        • `faculty` [str] - полное название факультета.

        • `year` [str] - год поступления группы.

        На выходе:

        • `list` всех групп данного факультета и года поступления.
        """
        year = str(year)
        self.driver.get(self.url)

        # Выбор периода времени в комбо-боксе
        select_period = Select(self.driver.find_element_by_xpath(
            '/html/body/div[4]/div[1]/div[2]/div/div[4]/div[1]/select'))
        select_period.select_by_value('2021-2022_2_1')
        time.sleep(1)

        # Выбор факультета в комбо-боксе
        select_faculty = Select(self.driver.find_element_by_xpath(
            '/html/body/div[4]/div[1]/div[2]/div/div[4]/div[2]/select'))
        select_faculty.select_by_value(faculty)
        time.sleep(1)

        # Выбор группы в комбо-боксе
        select_group = Select(self.driver.find_element_by_xpath(
            '/html/body/div[4]/div[1]/div[2]/div/div[4]/div[4]/select'))
        options = select_group.options

        # Заполнение списка всех групп из вариантов комбо-бокса
        options_by_year = []

        for option in options:
            options[options.index(option)] = option.text

        for option in options:
            if option.startswith(f'О-{year}') and option.endswith('Б'):
                options_by_year.append(option)

        return options_by_year

    def teacher(self, name: str):
        """Возвращает преподавателя по имени (информация и расписание)."""
        schedule = self.teacher_schedule_v2(name)

        if not schedule:
            return None

        info = self.teacher_info_v2(name)
        info['schedule'] = schedule
        return info

    def schedule_v2(self, group: str):
        no = '-'
        teacher = ''
        days = {'Понедельник': 'monday', 'Вторник': 'tuesday', 'Среда': 'wednesday',
                'Четверг': 'thursday', 'Пятница': 'friday', 'Суббота': 'saturday'}

        lesson_times = {
            '08:00 - 09:35': 1,
            '09:45 - 11:20': 2,
            '11:30 - 13:05': 3,
            '13:20 - 14:55': 4,
            '13:20 - 16:40': 4,
            '15:05 - 16:40': 5,
            '16:50 - 18:25': 6,
            '18:40 - 20:15': 7,
            '18:40 - 20:25': 7,
            '20:25 - 22:00': 8
        }

        weekday_model_ = {
            'even': [],
            'odd': [],
        }

        schedule = {
            'group': group,
            'last_updated': str(datetime.now()),
            'monday': deepcopy(weekday_model_),
            'tuesday': deepcopy(weekday_model_),
            'wednesday': deepcopy(weekday_model_),
            'thursday': deepcopy(weekday_model_),
            'friday': deepcopy(weekday_model_),
            'saturday': deepcopy(weekday_model_),
        }

        params = {
            'namedata': 'schedule',
            'group': group,
            'period': '2021-2022_2_1',
            'form': 'очная'
        }
        page = requests.get(self.url + '/schedule.ajax.php', params)
        soup = BeautifulSoup(page.text, 'html.parser')
        rows = soup.find_all('tr')

        row: Tag

        # Разделена ли ячейка
        splitted = False

        # Тип недели
        week_type = 'both'

        # Время пары
        time = ''

        for row in rows:
            #! День недели
            if row.select_one('.daeweek'):
                day = days[row.text]
                continue

            #! Время
            time_cell = row.select_one('.schtime')

            if not time_cell:
                # ? Времени нет => вторая пара в разделе
                splitted = False
                week_type = 'even'

            elif time_cell.has_attr('rowspan'):
                # ? Есть rowspan => первая пара в разделе
                time = time_cell.text.lstrip()
                index = lesson_times[time] - 1
                splitted = True
                week_type = 'odd'

            else:
                # ? Есть время, нет rowspan => обычная пара
                time = time_cell.text.lstrip()
                index = lesson_times[time] - 1
                week_type = 'both'
                splitted = False

            #! Предмет
            subject_cell = row.select_one('.schname')

            if not subject_cell.text:
                # ? Пары нет (окно)
                continue

            subject_name = subject_cell.contents[0].text
            subject_type = subject_cell.contents[2].text

            if subject_type == 'практическое занятие':
                subject = f"[ПЗ] {subject_name}"

            elif subject_type == 'лекция':
                subject = f"[Л] {subject_name}"

            elif subject_type == 'лабораторное занятие':
                subject = f"[ЛАБ] {subject_name}"

            #! Преподаватель
            teacher_cell = row.select_one('.schteacher')

            teacher = ', '.join([teacher.strip()
                                for teacher in teacher_cell.text.split('\n')])

            #! Аудитория
            room_cell = row.select_one('.schclass')
            room = room_cell.text

            #! Добавление данных в результирующий словарь
            lesson = {
                'number': index+1,
                'subject': subject,
                'room': room,
                'teacher': teacher
            }

            if week_type == 'both':
                schedule[day]['odd'].append(lesson)
                schedule[day]['even'].append(lesson)
            else:
                schedule[day][week_type].append(lesson)

        return schedule

    def news(self):
        url = self.base_url + "/info/press.rss/reviews"
        xml = requests.get(url)
        parser = RSSParser(xml=xml.content)
        feed = parser.parse()
