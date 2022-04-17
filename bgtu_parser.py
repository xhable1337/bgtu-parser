from datetime import datetime
import re
import time

from selenium import webdriver
from selenium.webdriver.support.ui import Select


class Parser:
    def __init__(self,
                 chromedriver_path: str = 'chromedriver.exe',
                 headless: bool = True) -> None:
        self.url = 'https://www.tu-bryansk.ru/education/schedule/'
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

    def schedule(self, group: str):
        """Получает расписание с сайта БГТУ.

        На входе:

        • `group` [str] - группа, для которой нужно получить расписание

        На выходе:

        • `dict` с расписанием группы на обе недели — чётную и нечётную.
        """
        no = '-'
        teacher = ''
        days = {'Понедельник': 'monday', 'Вторник': 'tuesday', 'Среда': 'wednesday',
                'Четверг': 'thursday', 'Пятница': 'friday', 'Суббота': 'saturday'}

        lesson_times = {
            '08:00 - 09:35': 1,
            '09:45 - 11:20': 2,
            '11:30 - 13:05': 3,
            '13:20 - 14:55': 4,
            '15:05 - 16:40': 5,
            '16:50 - 18:25': 6,
            '18:40 - 20:15': 7,
            '18:40 - 20:25': 7
        }

        weekday_model_ = {
            'even': [
                {
                    'number': i,
                    'subject': no,
                    'room': no,
                    'teacher': no
                }
                for i in range(1, 8)
            ],
            'odd': [
                {
                    'number': i,
                    'subject': no,
                    'room': no,
                    'teacher': no
                }
                for i in range(1, 8)
            ],
        }

        schedule = {
            'group': group,
            'last_updated': datetime.now(),
            'monday': weekday_model_,
            'tuesday': weekday_model_,
            'wednesday': weekday_model_,
            'thursday': weekday_model_,
            'friday': weekday_model_,
            'saturday': weekday_model_
        }

        self.driver.get(self.url)
        select_period = Select(self.driver.find_element_by_xpath(
            '/html/body/div[4]/div[1]/div[2]/div/div[4]/div[1]/select'))
        select_period.select_by_value('2021-2022_2_1')
        time.sleep(1)
        select_group = Select(self.driver.find_element_by_xpath(
            '/html/body/div[4]/div[1]/div[2]/div/div[4]/div[4]/select'))
        select_group.select_by_value(group)
        time.sleep(1)
        td = self.driver.find_elements_by_tag_name('td')
        iter_index = -1
        for i in td:
            td[td.index(i)] = i.text
        for i in td:
            iter_index += 1
            if i in days:
                it = 0
                day = days[i]
                subject, room, teacher = '', '', ''
            if re.match(r'\b\d\d:\d\d - \d\d:\d\d\b', i):
                it = 0
                index = lesson_times[i] - 1
            if '\n' in i and not re.fullmatch(r'([А-Яа-я]+. [А-Яа-я]. [А-Яа-я].(\n)*)+', str(i)):
                subject_type = i.split('\n')[1]
                subject = i.split('\n')[0]

                if subject_type == 'практическое занятие':
                    subject = f"[ПЗ] {subject}"

                elif subject_type == 'лекция':
                    subject = f"[Л] {subject}"

                elif subject_type == 'лабораторное занятие':
                    subject = f"[ЛАБ] {subject}"

                else:
                    subject = f"[{subject_type}] {subject}"
            if re.fullmatch(r'([А-Яа-я]+. [А-Яа-я]. [А-Яа-я].(\n)*)+', str(i)):
                teacher = ', '.join([teacher.strip()
                                    for teacher in str(i).split('\n')])
                print(f"{subject} - {teacher}")

            if (str(i).startswith('ауд. ')
                    or str(i) == 'спортзал'
                    or re.fullmatch(r'\b[АБВД]\b', str(i))
                    or re.fullmatch(r'\b[АБ]\d\d\d\b', str(i))
                    or re.fullmatch(r'\b\d\d\d\b', str(i))
                    or '/' in str(i)
                    or re.fullmatch(r'\b\d\d\d, *\d\d\d\b', str(i))
                    or str(i).upper() == 'УМ'
                    or re.fullmatch(r'\b\d\d\b', str(i))
                    or str(i).startswith('ч/')
                    ):
                room = str(i)
                if str(i).startswith('ауд. '):
                    room = room[5:]
                try:
                    if re.match(r'\b\d\d:\d\d - \d\d:\d\d\b', td[iter_index + 1]) or td[iter_index + 1] in days or i == td[-1]:
                        if it == 0:
                            schedule[day]['even'][index]['subject'] = subject
                            schedule[day]['even'][index]['room'] = room
                            schedule[day]['even'][index]['teacher'] = teacher
                            schedule[day]['odd'][index]['subject'] = subject
                            schedule[day]['odd'][index]['room'] = room
                            schedule[day]['odd'][index]['teacher'] = teacher
                            subject, room, teacher = '', '', ''
                        else:
                            schedule[day]['odd'][index]['subject'] = subject
                            schedule[day]['odd'][index]['room'] = room
                            schedule[day]['odd'][index]['teacher'] = teacher
                            subject, room, teacher = '', '', ''
                            it = 0
                    elif td[iter_index + 1] == '':
                        if it == 0:
                            schedule[day]['even'][index]['subject'] = subject
                            schedule[day]['even'][index]['room'] = room
                            schedule[day]['even'][index]['teacher'] = teacher
                            schedule[day]['odd'][index]['subject'] = subject
                            schedule[day]['odd'][index]['room'] = room
                            schedule[day]['odd'][index]['teacher'] = teacher
                            subject, room, teacher = '', '', ''
                        else:
                            schedule[day]['odd'][index]['subject'] = subject
                            schedule[day]['odd'][index]['room'] = room
                            schedule[day]['odd'][index]['teacher'] = teacher
                            subject, room, teacher = '', '', ''
                            it = 0
                    else:
                        schedule[day]['even'][index]['subject'] = subject
                        schedule[day]['even'][index]['room'] = room
                        schedule[day]['even'][index]['teacher'] = teacher
                        subject, room, teacher = '', '', ''
                        it += 1
                except IndexError:
                    if i == td[-1]:
                        if it == 0:
                            schedule[day]['even'][index]['subject'] = subject
                            schedule[day]['even'][index]['room'] = room
                            schedule[day]['even'][index]['teacher'] = teacher
                            schedule[day]['odd'][index]['subject'] = subject
                            schedule[day]['odd'][index]['room'] = room
                            schedule[day]['odd'][index]['teacher'] = teacher
                            subject, room, teacher = '', '', ''
                        else:
                            schedule[day]['odd'][index]['subject'] = subject
                            schedule[day]['odd'][index]['room'] = room
                            schedule[day]['odd'][index]['teacher'] = teacher
                            subject, room, teacher = '', '', ''
                            it = 0
            if i == '':
                td[iter_index], td[iter_index +
                                   1], td[iter_index + 2] = no, 'Nobody N. O.', no
                if re.match(r'\b\d\d:\d\d - \d\d:\d\d\b', td[iter_index - 1]):
                    subject, room = no, no
                    schedule[day]['even'][index]['subject'] = subject
                    schedule[day]['even'][index]['room'] = room
                    schedule[day]['even'][index]['teacher'] = subject, room, teacher
                    subject, room, teacher = '', '', ''
                    it += 1
                elif str(td[iter_index - 1]).startswith('ауд. ') or str(td[iter_index - 1]) or re.fullmatch(r'\b[АБВД]\b', str(td[iter_index - 1])) or re.fullmatch(r'\b[АБ]\d\d\d\b', str(td[iter_index - 1])) or re.fullmatch(r'\b\d\d\d\b', str(td[iter_index - 1])) or re.fullmatch(r'\b\d\d\d, *\d\d\d\b', str(td[iter_index - 1])) or str(td[iter_index - 1]).upper() == 'УМ' or re.fullmatch(r'\b\d\d\b', str(td[iter_index - 1])) == 'спортзал' or str(td[iter_index - 1]).startswith('ч/'):
                    subject, room = no, no
                    schedule[day]['odd'][index]['subject'] = subject
                    schedule[day]['odd'][index]['room'] = room
                    schedule[day]['odd'][index]['teacher'] = teacher
                    subject, room, teacher = '', '', ''
                    it = 0
        iter_index = 0
        schedule['last_updated'] = datetime.now()

        return schedule
