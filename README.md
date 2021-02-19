# [bgtu-parser](https://github.com/xhable1337/bgtu-parser) ­­— brand new parser for obtaining schedule <!-- omit in toc -->

----------

# Table of contents <!-- omit in toc -->
- [Requirements](#requirements)
- [How to launch](#how-to-launch)
- [How to use](#how-to-use)
- [How to make requests](#how-to-make-requests)
  - [Requests list](#requests-list)
  - [About password in pseudo-security purposes](#about-password-in-pseudo-security-purposes)
- [To-do list](#to-do-list)
- [Credits](#credits)

----------

# Requirements
- [Selenium](https://pypi.org/project/selenium/) — `pip install selenium`
- [Flask](https://pypi.org/project/Flask/) — `pip install flask`

----------

# How to launch
1. Open Terminal or cmd
2. Change directory to one which contains the app with the `cd` command
3. Install all dependencies from `requirements.txt`: `pip install -r requirements.txt` ([or manually](#requirements))
4. Run parser: `python app.py`

----------

# How to use
1. Launch parser
2. Open http://localhost:8443/ in your browser
3. If there is “OK” string, then all is in working state. You are ready to make some requests.

----------

# How to make requests
## Requests list
There are **two** types of requests at the moment:
1. Get schedule: `get_schedule(group)`
`http://localhost:8443/sample_value/get_schedule?group=group`, where `group` parameter is your group.
2. Get group list: `get_groups(faculty, year)`
`http://localhost:8443/sample_value/get_groups?faculty=faculty&year=year`, where `faculty` and `year` — your parameters.

There are all of the requests you can perform, using [bgtu-parser](https://github.com/xhable1337/bgtu-parser).

## About password in pseudo-security purposes
For example, you would like to get a schedule for group named “О-20-ИВТ-1-по-Б”. Then your request will look like this:
`http://localhost:8443/sample_value/get_schedule?group=О-20-ИВТ-1-по-Б`, where `sample_value` is a kinda dumb password. You can change it inside the code by changing [corresponding variable named `password`](https://github.com/xhable1337/bgtu-parser/blob/ed3dbff6a5f800c53ce22b3000f2803dd08799b9/app.py#L39).


----------

# To-do list
- [x] Create a parser, fill it with basic function — obtaining schedule
- [x] Add obtaining the group list feature
- [x] Refactor all the code so it don’t look messy and full of unnecessary comments
- [ ] Add a function to get a departments, faculties and infromation about them
- [ ] Add a feature to get information about teachers and their schedule

----------

# Credits
All credits goes to [xhable1337](https://github.com/xhable1337), author of this repository. 