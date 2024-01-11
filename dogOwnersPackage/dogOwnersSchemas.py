from typing import Union
from pydantic import BaseModel



#dog_owner base
class DogOwnerBase(BaseModel):
    id: int
    username: str
    about_me: str
    
    
#create a dog owner
class DogOwnerCreate(BaseModel):
    username: str
    about_me: str
    
    
#update dog owner about_me
class DogOwnerUpdate(BaseModel):
    about_me: str
    
    
#for one dog owner
class DogOwner(DogOwnerBase):
    
    class Config:
        orm_mode = True