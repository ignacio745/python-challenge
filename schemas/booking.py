from datetime import datetime, time
from typing import Optional
from pydantic import BaseModel


class Booking(BaseModel):
    origin: str
    destination: str
    dep_date_time: datetime
    duration: time

    class Config:
        orm_mode = True


class BookingUpdate(BaseModel):
    origin: Optional[str]
    destination: Optional[str]
    dep_date_time: Optional[datetime]
    duration: Optional[time]


class BookingResponse(Booking):
    id: int