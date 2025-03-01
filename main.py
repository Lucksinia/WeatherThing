from sqlmodel import SQLModel, Field, Session, create_engine, select
from fastapi import FastAPI, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import timezone, datetime
import uvicorn
import dotenv
import httpx
import os

dotenv.load_dotenv(".env")

DATABASE_URL = os.getenv("DATABASE_URL")

WEATHER_API_URL = os.getenv("API")

API_KEY = os.getenv("OPENWEATHER_API")


# db stuff
class WeatherQuery(SQLModel, table=True):
    __tablename__ = "WeatherQuery"
    __table_args__ = {"extend_existing": True}  # hack for already created db
    id: int = Field(default=None, primary_key=True)
    city_name: str | None = Field(default=None, index=True)
    # special datetime funny, because utcnow is deprecated.
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    temperature: float | None
    description: str | None
    icon: str | None = Field(default="o1d")


app = FastAPI()
engine = create_engine(DATABASE_URL)
templates = Jinja2Templates(directory="templates")

# Create tables if not exist
SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


# Just to save on the characters that I need to type.
@app.get("/", response_class=RedirectResponse)
async def redirect():
    return RedirectResponse("/weather")


@app.get("/weather")
async def get_weather_page(request: Request):
    return templates.TemplateResponse("weather.html", {"request": request})


@app.post("/weather")
async def fetch_weather(
    request: Request,
    city_name: str = Form(...),
    session: Session = Depends(get_session),
):
    params = {"q": city_name, "appid": API_KEY, "units": "metric"}
    async with httpx.AsyncClient() as client:
        response = await client.get(WEATHER_API_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    weather_data = response.json()

    if response.status_code == 200:
        temperature = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]
        icon = weather_data["weather"][0]["icon"]
        # Save to database if succsessfull
        weather_query = WeatherQuery(
            city_name=city_name,
            temperature=temperature,
            description=description,
            icon=icon,
        )
        session.add(weather_query)

        session.commit()
        session.refresh(weather_query)

        return templates.TemplateResponse(
            "weather.html",
            {
                "request": request,
                "city": city_name,
                "temperature": temperature,
                "description": description,
                "timestamp": weather_query.timestamp,
                "icon": icon,
            },
        )


@app.get("/history")
async def get_history(request: Request, session: Session = Depends(get_session)):
    results = session.exec(select(WeatherQuery)).all()
    return templates.TemplateResponse(
        "queries.html", {"request": request, "data": results}
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
