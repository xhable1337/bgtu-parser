<h1 align=center><a href="https://github.com/xhable1337/bgtu-parser">bgtu-parser</a> — brand new parser for obtaining schedule</h1>

<h2 align=center>v2.1.2 — rebase to FastAPI, refactoring</h2>

# Table of contents

- [Requirements](#requirements)
- [How to launch](#how-to-launch)
- [How to use](#how-to-use)
- [How to make requests](#how-to-make-requests)
  - [Requests list](#requests-list)
- [To-do list](#to-do-list)
- [Credits](#credits)

# Requirements

- [Selenium](https://pypi.org/project/selenium/) — `pip install selenium`
- [FastAPI](https://pypi.org/project/fastapi/) — `pip install fastapi`
- [pydantic](https://pypi.org/project/pydantic/) — `pip install pydantic`
- [uvicorn](https://pypi.org/project/uvicorn/) — `pip install uvicorn`

# How to launch

1. Open Terminal or cmd
2. Change directory to one which contains the app with the `cd` command
3. Install all dependencies from `requirements.txt`: `pip install -r requirements.txt` ([or manually](#requirements))
4. Run parser: `python app.py`

# How to use

1. Launch parser
2. Open http://localhost:8443/ in your browser
3. If there is a documentation on the index page, then all systems are operational. You are ready to make some requests.

# How to make requests

Basically, you can use built-in Swagger UI to interact with API, but the most common way is to make request from another program.

## Requests list

There are **two** types of requests at the moment:

1. Get schedule: `get_schedule(group)`
   `http://localhost:8443/api/v2/schedule?group=group`, where `group` parameter is your group.
2. Get group list: `get_groups(faculty, year)`
   `http://localhost:8443/api/v2/groups?faculty=faculty&year=year`, where `faculty` and `year` — your parameters.

There are all of the requests you can perform, using [bgtu-parser](https://github.com/xhable1337/bgtu-parser).

# To-do list

- [x] Create a parser, fill it with basic function — obtaining schedule
- [x] Add obtaining the group list feature
- [x] Refactor all the code so it doesn’t look messy and full of unnecessary comments
- [x] Rebase on [FastAPI](https://fastapi.tiangolo.com)
- [x] Add a feature to get information about teachers and their schedule
- [ ] Add a function to get a departments, faculties and information about them

# Credits

All credits goes to [xhable1337](https://github.com/xhable1337), author of this repository.
