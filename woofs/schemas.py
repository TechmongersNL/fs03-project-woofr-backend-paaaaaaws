
from typing import Union
from pydantic import BaseModel
import datetime



#woof base
class WoofBase(BaseModel):
    id: int
    message: str
    created_at: datetime.datetime
    
#create a woof
class WoofCreate(BaseModel):
    message: str
    
#for one woof 
class Woof(WoofBase):
    
    class Config:
        orm_mode = True