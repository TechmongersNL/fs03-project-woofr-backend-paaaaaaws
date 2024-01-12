import os
from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import dogOwnersSchemas
from app import models
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from typing import Union, Any
from dotenv import load_dotenv

load_dotenv()

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']

# for auth


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def login_owner(db: Session, dog_owner_credentials: dogOwnersSchemas.DogOwnerCredentials):
    db_owner = db.query(models.Dog_owner).filter(
        models.Dog_owner.email == dog_owner_credentials.email).first()

    user_password_error = "Incorrect username or password"

    if db_owner is None:
        raise HTTPException(status_code=404, detail=user_password_error)
    if not verify_password(dog_owner_credentials.password, db_owner.password_hash):
        raise HTTPException(status_code=401, detail=user_password_error)
    return {"access_token": create_access_token(f"{db_owner.id}:{db_owner.email}"),
            "token_type": "bearer"}

# get_owner


def get_owner(db: Session, dog_owner_id: int):
    dog_owner = db.query(models.Dog_owner).filter(
        models.Dog_owner.id == dog_owner_id).first()
    print(dog_owner)
    return dog_owner

# get_owners


def get_owners(db: Session, skip: int = 0, limit: int = 20):
    owners = db.query(models.Dog_owner).offset(skip).limit(limit).all()
    print(owners)
    return owners

# create_owner


def create_owner(db: Session, dog_owner: dogOwnersSchemas.DogOwnerCreate):
    password_hash = get_hashed_password(password=dog_owner.password)
    db_owner = models.Dog_owner(
        email=dog_owner.email, password_hash=password_hash)
    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)
    return db_owner

# update owner username and about_me sections


def update(db: Session, dog_owner_id: int, updated_data: dogOwnersSchemas.DogOwnerUpdate):
    existing_owner = db.query(models.Dog_owner).filter(
        models.Dog_owner.id == dog_owner_id).first()

    if existing_owner:
        for key, value in updated_data.dict().items():
            setattr(existing_owner, key, value)

        db.commit()
        db.refresh(existing_owner)

    return existing_owner

# delete owner


def delete_owner(db: Session, dog_owner_id: int):
    owner = db.query(models.Dog_owner).filter(
        models.Dog_owner.id == dog_owner_id).first()
    db.delete(owner)
    db.commit()
    return owner
