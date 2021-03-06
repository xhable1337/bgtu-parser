"""Парсер сайта БГТУ, который позволяет получать расписание и список групп.

Возможности:

• `get_schedule(group)` - получить список с расписанием для заданной группы.

• `get_groups(faculty, year)` - получить список групп по заданным факультету и году.
"""

from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import datetime
import os
import re
import time

CHROMEDRIVER_PATH = 'chromedriver.exe'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--disable-browser-side-navigation')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.206 (Edition Yx GX)")
#chrome_options.binary_location = CHROME_BIN
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
driver.implicitly_wait(10)

#firefox_options.headless = True
#firefox_options = webdriver.FirefoxOptions()

server = Flask(__name__)
password = 'sample_value' # Импровизированный пароль для предотвращения спама запросами к сайту БГТУ
url = 'https://www.tu-bryansk.ru/education/schedule/' # URL сайта БГТУ, раздел с расписанием

def get_groups(faculty='Факультет информационных технологий', year='20'):
    """Получает список групп по заданному факультету с сайта БГТУ, помещает в базу данных и выводит как результат функции.

    На входе:

    • `faculty` [str] - полное название факультета.

    • `year` [str] - год поступления группы.

    • `force_update` [bool] - принудительно обновить список групп в базе.

    На выходе:
    
    • `list` всех групп данного факультета и года поступления.
    """
    year = str(year)
    
    #driver.implicitly_wait(10)
    driver.get(url) 
    select_period = Select(driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div/div[4]/div[1]/select'))
    select_period.select_by_value('2020-2021_2_1')
    time.sleep(1)
    select_faculty = Select(driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div/div[4]/div[2]/select'))
    select_faculty.select_by_value(faculty)
    time.sleep(1)

    select_group = Select(driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div/div[4]/div[4]/select'))
    options = select_group.options
    options_by_year = []

    for option in options:
            options[options.index(option)] = option.text

    for option in options:
        if option.startswith(f'О-{year}') and option.endswith('Б'):
            options_by_year.append(option)

    return options_by_year

def get_schedule(group):
    """Получает расписание с сайта БГТУ.

    На входе: 
    
    • `group` [str] - группа, для которой нужно получить расписание

    На выходе:

    • `dict` с расписанием группы на обе недели — чётную и нечётную.
    """
    no = '-'
    days = {'Понедельник': 'monday', 'Вторник': 'tuesday', 'Среда': 'wednesday', 'Четверг': 'thursday', 'Пятница': 'friday', 'Суббота': 'saturday'}
    lesson_times = {'08:00 - 09:35': 1, '09:45 - 11:20': 2, '11:30 - 13:05': 3, '13:20 - 14:55': 4, '15:05 - 16:40': 5}
    schedule = {
    'group': group,
    'last_updated': time.time(),
    'monday': {'1': [[1, no, no], [2, no, no], [3, no, no], [4, no, no], [5, no, no]], '2': [[1, no, no], [2, no, no], [3, no, no], [4, no, no], [5, no, no]]},
    'tuesday': {'1': [[1, no, no], [2, no, no], [3, no, no], [4, no, no], [5, no, no]], '2': [[1, no, no], [2, no, no], [3, no, no], [4, no, no], [5, no, no]]},
    'wednesday': {'1': [[1, no, no], [2, no, no], [3, no, no], [4, no, no], [5, no, no]], '2': [[1, no, no], [2, no, no], [3, no, no], [4, no, no], [5, no, no]]},
    'thursday': {'1': [[1, no, no], [2, no, no], [3, no, no], [4, no, no], [5, no, no]], '2': [[1, no, no], [2, no, no], [3, no, no], [4, no, no], [5, no, no]]},
    'friday': {'1': [[1, no, no], [2, no, no], [3, no, no], [4, no, no], [5, no, no]], '2': [[1, no, no], [2, no, no], [3, no, no], [4, no, no], [5, no, no]]},
    'saturday': {'1': [[1, no, no], [2, no, no], [3, no, no], [4, no, no], [5, no, no]], '2': [[1, no, no], [2, no, no], [3, no, no], [4, no, no], [5, no, no]]}
    }

    #driver.implicitly_wait(10)
    driver.get(url)
    select_period = Select(driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div/div[4]/div[1]/select'))
    select_period.select_by_value('2020-2021_2_1')
    time.sleep(1)
    select_group = Select(driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div/div[4]/div[4]/select'))
    select_group.select_by_value(group)
    time.sleep(1)
    td = driver.find_elements_by_tag_name('td')
    iter_index = -1
    for i in td:
        td[td.index(i)] = i.text
    for i in td:
        iter_index += 1
        if i in days:
            it = 0
            day = days[i]
            subject, room = '', ''
        if re.match(r'\b\d\d:\d\d - \d\d:\d\d\b', i):
            it = 0
            index = lesson_times[i] - 1
        if '\n' in i and not re.fullmatch(r'([А-Яа-я]+. [А-Яа-я]. [А-Яа-я].(\n)*)+', str(i)):
            print(f'{td.index(i)}) {i}')
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
        if str(i).startswith('ауд. ') or str(i) == 'спортзал' or re.fullmatch(r'\b[АБВД]\b', str(i)) or re.fullmatch(r'\b[АБ]\d\d\d\b', str(i)) or re.fullmatch(r'\b\d\d\d\b', str(i)) or re.fullmatch(r'\b\d\d\d, *\d\d\d\b', str(i)) or str(i).upper() == 'УМ' or re.fullmatch(r'\b\d\d\b', str(i)) or str(i).startswith('ч/'):
            room = str(i)
            if str(i).startswith('ауд. '):
                room = room[5:]
            try:
                if re.match(r'\b\d\d:\d\d - \d\d:\d\d\b', td[iter_index + 1]) or td[iter_index + 1] in days or i == td[-1]:
                    if it == 0:
                        schedule[day]['1'][index][1], schedule[day]['1'][index][2] = subject, room
                        schedule[day]['2'][index][1], schedule[day]['2'][index][2] = subject, room
                        subject, room = '', ''
                    else:
                        schedule[day]['2'][index][1], schedule[day]['2'][index][2] = subject, room
                        subject, room = '', ''
                        it = 0
                elif td[iter_index + 1] == '':
                    if it == 0:
                        schedule[day]['1'][index][1], schedule[day]['1'][index][2] = subject, room
                        schedule[day]['2'][index][1], schedule[day]['2'][index][2] = subject, room
                        subject, room = '', ''
                    else:
                        schedule[day]['2'][index][1], schedule[day]['2'][index][2] = subject, room
                        subject, room = '', ''
                        it = 0
                else:
                    schedule[day]['1'][index][1], schedule[day]['1'][index][2] = subject, room
                    subject, room = '', ''
                    it += 1
            except IndexError:
                if i == td[-1]:
                    if it == 0:
                        schedule[day]['1'][index][1], schedule[day]['1'][index][2] = subject, room
                        schedule[day]['2'][index][1], schedule[day]['2'][index][2] = subject, room
                        subject, room = '', ''
                    else:
                        schedule[day]['2'][index][1], schedule[day]['2'][index][2] = subject, room
                        subject, room = '', ''
                        it = 0
        if i == '':    
            td[iter_index], td[iter_index + 1], td[iter_index + 2] = no, 'Nobody N. O.', no
            if re.match(r'\b\d\d:\d\d - \d\d:\d\d\b', td[iter_index - 1]):
                subject, room = no, no
                schedule[day]['1'][index][1], schedule[day]['1'][index][2] = subject, room
                subject, room = '', ''
                it += 1
            elif str(td[iter_index - 1]).startswith('ауд. ') or str(td[iter_index - 1]) or re.fullmatch(r'\b[АБВД]\b', str(td[iter_index - 1])) or re.fullmatch(r'\b[АБ]\d\d\d\b', str(td[iter_index - 1])) or re.fullmatch(r'\b\d\d\d\b', str(td[iter_index - 1])) or re.fullmatch(r'\b\d\d\d, *\d\d\d\b', str(td[iter_index - 1])) or str(td[iter_index - 1]).upper() == 'УМ' or re.fullmatch(r'\b\d\d\b', str(td[iter_index - 1])) == 'спортзал' or str(td[iter_index - 1]).startswith('ч/'):
                subject, room = no, no
                schedule[day]['2'][index][1], schedule[day]['2'][index][2] = subject, room
                subject, room = '', ''
                it = 0
    iter_index = 0
    schedule['last_updated'] = time.time()

    return schedule

@server.route('/')
def index_page():
    return "OK", 200

@server.route('/' + password + '/get_schedule/')
def schedule_api():
    group = request.args.get('group')
    
    if group is None:
        group = 'О-20-ИВТ-1-по-Б'
        
    schedule = get_schedule(group)
    return str(schedule), 200

@server.route("/" + password + '/get_groups/')
def groups_api():
    faculty = request.args.get('faculty')
    if faculty is None:
        faculty = 'Факультет информационных технологий'

    year = request.args.get('year')
    if year is None:
        year = '20'
    
    groups = get_groups(faculty, year)
    return str(groups), 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', '8443')))