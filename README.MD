# WeatherThing #

This is a quick and cluncky Python web applet, made with ___Postgres___, ___FastAPI___ and __Python 3.12.5__, in one file.

## To Start ##

1. Create virtual environment with `python -m venv <your-venv-name>` and activate it.
2. Install all dependencies with `pip install -r 'req.txt'`.
3. Create your Postgres database.
4. Create _.env_ file for your secrets. Here is an example:

    ```shell
    OPENWEATHER_API = <Your-API-Key>

    # Because I can't look at 3.0 docs, I used http://api.openweathermap.org/data/2.5/weather
    API = <API-URL-HERE>

    DATABASE_URL =postgresql://<login>:<password>@localhost/<table-name>
    ```

5. Run `python main.py` in your terminal. It  will start on `http://localhost:8000/` with hot reload __on__.
6. Use web app interface as you want!

## Examples ##

Examples:

| Main | History |
| ----------- | ----------- |
| ![index](/img/MainInterfacePic.png) | ![QueryHistory](/img/History.png)|

## Used libraries ##

Python-Dotenv, FastAPI, Jinja2, SQLModel, uvicorn, httpx
