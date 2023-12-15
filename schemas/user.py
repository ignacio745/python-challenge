from typing import Optional
from pydantic import BaseModel, EmailStr
from .booking import Booking


class UserBase(BaseModel):
    email: EmailStr


class User(UserBase):
    bookings: list[Booking] = []
    
    class Config:
        orm_mode = True


class UserCreate(UserBase):
    name: str
    password: str


class UserSignIn(UserBase):
    password: str


class UserUpdate(BaseModel):
    old_email: EmailStr
    new_email: Optional[EmailStr]
    name: Optional[str]
    old_password: str
    new_password: Optional[str]