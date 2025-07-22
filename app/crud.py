from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas

async def create_weather_query(db: AsyncSession, weather_data: schemas.WeatherQueryRead):
    db_item = models.WeatherQuery(
        city=weather_data.city,
        temperature=weather_data.temperature,
        description=weather_data.description
    )
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

async def get_weather_history(db: AsyncSession):
    result = await db.execute(select(models.WeatherQuery).order_by(models.WeatherQuery.timestamp.desc()))
    return result.scalars().all()
