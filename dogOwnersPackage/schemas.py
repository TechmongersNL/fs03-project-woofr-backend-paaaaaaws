from typing import Union
from pydantic import BaseModel
import datetime



#dog_owner base
class DogOwnerBase(BaseModel):
    id: int
    username: str
    about_me: str
    
    
#create a dog owner
class DogOwnerCreate(BaseModel):
    username: str
    about_me: str
    
class DogOwnerUpdate(BaseModel):
    username:str
    about_me: str
    
#for one dog owner
class DogOwner(DogOwnerBase):
    
    class Config:
        orm_mode = True