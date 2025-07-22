from pydantic import BaseModel
from datetime import datetime

class WeatherQueryCreate(BaseModel):
    city: str

class WeatherQueryRead(BaseModel):
    id: int
    city: str
    temperature: float
    description: str
    timestamp: datetime

    class Config:
        orm_mode = True
