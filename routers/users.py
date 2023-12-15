from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.user import User as User, UserCreate, UserSignIn, UserUpdate
from database.database import get_db
from crud import user_crud


user_router = APIRouter(prefix="/user", tags=["Users"])


@user_router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.create_user(db=db, user=user)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    return db_user


@user_router.put("/", response_model=User)
def update_user(user:UserUpdate, db: Session = Depends(get_db)):
    updated =  user_crud.update_user(db=db, user=user)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong email or password"
        )
    return updated


@user_router.delete("/")
def delete_user(user: UserSignIn, db: Session = Depends(get_db)):
    deleted = user_crud.delete_user(db=db, user=user)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong email or password"
        )
    return {
        "message": "User deleted"
    }