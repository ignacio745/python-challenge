from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from models.user import User as DBUser
from security.hash_password import verify_hash
from security import oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from crud import user_crud


auth_router = APIRouter(tags=["Authentication"])


@auth_router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(DBUser).filter(DBUser.email == user_credentials.username).first()
    user = user_crud.get_user_by_email(db, user_email=user_credentials.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    if not verify_hash(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    

    access_token = oauth2.create_access_token(data= {"user_id": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }