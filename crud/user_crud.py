from sqlalchemy.orm import Session
from models.user import User as DBUser
from schemas.user import UserCreate, UserUpdate, UserSignIn
from security.hash_password import create_hash, verify_hash
from security import hash_password


def get_user_by_email(db: Session, user_email):
    dbuser = db.query(DBUser).filter(DBUser.email == user_email).first()
    if not dbuser:
        return False
    return dbuser


def create_user(db: Session, user: UserCreate):
    user_exist = db.query(DBUser).filter(DBUser.email == user.email).first()
    if user_exist:
        return False
    hashed_password = create_hash(user.password)
    db_user = DBUser(email=user.email, name=user.name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: UserUpdate):
    user_to_update = db.query(DBUser).filter(DBUser.email == user.old_email).first()
    if not user_to_update:
        return False
    if not hash_password.verify_hash(user.old_password, user_to_update.hashed_password):
        return False
    if user.new_email:
        user_to_update.email = user.new_email
    if user.new_password:
        user_to_update.hashed_password = hash_password.create_hash(user.new_password)
    user_to_update.name = user.name
    db.commit()
    db.refresh(user_to_update)
    return user_to_update


def delete_user(db: Session, user: UserSignIn):
    user_to_delete = db.query(DBUser).filter(DBUser.email == user.email).first()
    if not user_to_delete:
        return False
    if not hash_password.verify_hash(user.password, user_to_delete.hashed_password):
        return False
    db.delete(user_to_delete)
    db.commit()
    return True
    

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_hash(password, user.hashed_password):
        return False
    return user