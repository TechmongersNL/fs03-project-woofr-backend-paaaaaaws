import os
from passlib.context import CryptContext
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Annotated, Union, Any
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app import models, database
from sqlalchemy.orm import Session
from . import dogOwnersSchemas, dogOwners

load_dotenv()

# Token encoding configuration
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']

# Authorized request configuration
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/docslogin", scheme_name="JWT")

# Authentication functions


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
    return {"access_token": create_access_token(db_owner.id),
            "token_type": "bearer"}


async def get_current_owner(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        db = database.SessionLocal()

        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        dog_owner_id: str = payload.get("sub")
        if dog_owner_id is None:
            raise credentials_exception
        token_data = dogOwnersSchemas.TokenPayload(id=dog_owner_id)
    except JWTError:
        raise credentials_exception
    owner = dogOwners.get_owner(db, dog_owner_id=token_data.id)
    if owner is None:
        raise credentials_exception
    return owner
