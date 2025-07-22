import httpx
import os
from dotenv import load_dotenv
load_dotenv()
from app.database import async_session
from app.models import WeatherQuery
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


async def fetch_weather_and_save(city: str):
    print("🔍 Запрос на город:", city)
    print("🔑 API_KEY:", API_KEY)
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }

    async with httpx.AsyncClient() as client:
        resp = await client.get(BASE_URL, params=params)
        print("🔍 HTTP status from OpenWeather:", resp.status_code)
        data = resp.json()
        print("🔍 Data from OpenWeather:", data)

        if resp.status_code != 200:
            return None

        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]

    # Сохранение в базу
    async with async_session() as session:
        async with session.begin():
            weather_query = WeatherQuery(
                city=city,
                temperature=temp,
                description=description,
                timestamp=datetime.utcnow()
            )
            session.add(weather_query)
        await session.commit()

    return {
        "city": city,
        "temperature": temp,
        "description": description
    }
