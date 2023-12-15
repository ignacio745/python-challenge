from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.database import get_db
from crud import booking_crud
from models.user import User as DBUser
from schemas.booking import Booking, BookingUpdate, BookingResponse
from security import oauth2
import datetime


booking_router = APIRouter(prefix="/booking", tags=["Bookings"])


@booking_router.get("/", response_model=list[BookingResponse])
def read_bookings(db: Session = Depends(get_db), current_user: DBUser = Depends(oauth2.get_current_user)):
    bookings = booking_crud.get_bookings(db, current_user.id)
    return bookings


@booking_router.get("/{id}", response_model=BookingResponse)
def read_booking(id: int, db: Session = Depends(get_db), current_user: DBUser = Depends(oauth2.get_current_user)):
    booking = booking_crud.get_booking(db, id, current_user.id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    return booking


@booking_router.post("/", response_model=BookingResponse)
def create_booking(booking: Booking, db: Session = Depends(get_db), current_user: DBUser = Depends(oauth2.get_current_user)):
    if booking.dep_date_time.replace(tzinfo=None) < datetime.datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The date and time sent has already passed"
        )
    id = int(current_user.id)
    return booking_crud.create_user_booking(db, booking, id)


@booking_router.put("/{id}", response_model=BookingResponse)
def update_booking(id: int, booking:BookingUpdate, db: Session = Depends(get_db), current_user: DBUser = Depends(oauth2.get_current_user)):
    if booking.dep_date_time and booking.dep_date_time < datetime.datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The date and time sent has already passed"
        )
    updated = booking_crud.update_booking(db, booking, id, current_user.id)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    return updated


@booking_router.delete("/{id}")
def delete_booking(id: int, db: Session = Depends(get_db), current_user: DBUser = Depends(oauth2.get_current_user)):
    deleted = booking_crud.delete_booking(db, id, current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    return {
        "message": "Booking deleted"
    }