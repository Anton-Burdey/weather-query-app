from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy.future import select
from sqlalchemy.exc import OperationalError
import asyncio
import asyncpg


from app.database import async_session, Base, engine
from app.weather import fetch_weather_and_save

app = FastAPI()

class WeatherRequest(Base):
    __tablename__ = "weather_requests"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    temperature = Column(Float)
    description = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

# Функция для ожидания доступности БД
async def wait_for_db():
    while True:
        try:
            async with engine.begin() as conn:
                await conn.run_sync(lambda conn: None)  # пробный запрос
            break  # если подключение успешно - выходим из цикла
        except (OperationalError, asyncpg.exceptions.CannotConnectNowError):
            print("База данных ещё не готова, повтор через 1 секунду...")
            await asyncio.sleep(1)

@app.on_event("startup")
async def startup():
    await wait_for_db()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with async_session() as session:
        yield session

@app.get("/")
async def root():
    return {"message": "Weather Query API is working"}

@app.post("/weather/")
async def get_weather(city: str, db: AsyncSession = Depends(get_db)):
    result = await fetch_weather_and_save(city)
    if not result:
        raise HTTPException(status_code=404, detail="City not found or API error")

    weather_record = WeatherRequest(
        city=result["city"],
        temperature=result["temperature"],
        description=result["description"],
    )
    db.add(weather_record)
    await db.commit()

    return result

@app.get("/history/")
async def get_history(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(WeatherRequest).order_by(WeatherRequest.timestamp.desc()))
    history = result.scalars().all()
    return history
