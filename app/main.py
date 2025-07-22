from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session, Base, engine
from app import models

app = FastAPI()

# Создание таблиц
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Зависимость
async def get_db():
    async with async_session() as session:
        yield session

@app.get("/")
async def root():
    return {"message": "Weather Query API is working"}
