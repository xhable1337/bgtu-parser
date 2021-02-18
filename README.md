# bgtu-parser

## How to launch
1. Open Terminal or cmd
2. Change directory to one which contains the app with the `cd` command
3. Install all dependencies: `pip install -r requirements.txt`
4. Run parser: `python app.py`

## How to use
1. Launch parser
2. Open http://localhost:8443/ in your browser
3. If there is "OK" string, then all is in working state. You are ready to make some requests.

## How to make requests
There are two types of requests at the moment:
1. Get schedule: `get_schedule(group)`
2. Get group list: `get_groups(faculty, year)`

For example, you would like to get a schedule for group named "О-20-ИВТ-1-по-Б". Then your request will look like this:
`http://localhost:8443/sample_value/get_schedule?group=О-20-ИВТ-1-по-Б`, where `sample_value` is a kinda dumb password. You can change it inside the code by changing corresponding variable named `password`: https://github.com/xhable1337/bgtu-parser/blob/20f5ca3c175d2aafd081dbd13cadeaa5bf4bfea7/app.py#L59

That's how requests are did. Just a GET requests with some parameters, pointed off in requests list a couple lines above.
