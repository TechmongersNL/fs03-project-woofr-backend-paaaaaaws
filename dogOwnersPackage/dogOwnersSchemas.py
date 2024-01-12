from typing import Union
from pydantic import BaseModel


# dog_owner base
class DogOwnerBase(BaseModel):
    id: int
    username: str
    about_me: str
    email: str


# create a dog owner on sign up
class DogOwnerCreate(BaseModel):
    email: str
    password: str


# credentials for dog owner
class DogOwnerCredentials(DogOwnerCreate):
    pass


# update dog owner about_me
class DogOwnerUpdate(BaseModel):
    userame: str
    about_me: str


# for one dog owner
class DogOwner(DogOwnerBase):

    class Config:
        orm_mode = True


# token pydantic models
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    exp: int
    sub: str
