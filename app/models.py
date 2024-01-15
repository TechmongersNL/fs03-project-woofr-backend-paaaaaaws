from app.database import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
import sys
import os
import datetime

# Routing to the app directory
path = os.path.abspath("app")
sys.path.append(path)

#are the posts!
class Woof(Base):
    __tablename__ = "woofs"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    description = Column(String)
    image=Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    dog_id=Column(Integer,ForeignKey("dogs.id"),nullable=False)

# From now on, Woofs belong to Dogs.
    dog=relationship("Dog",back_populates="woofs")
    


class DogOwner(Base): #camelCase
    __tablename__ = "dog_owners"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, unique=True, index=True)
    about_me = Column(String)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    # Dogs belong to DogOwner``
    dogs=relationship("Dog",back_populates="owner")
    
   
class Dog(Base):
    __tablename__="dogs"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name=Column(String, nullable=False)
    age=Column(Integer)
    owner_id=Column(Integer,ForeignKey("dog_owners.id"),nullable =False)
    # ^ always goes on the table where there is only one relationship (a relationship is singular)

    
    # DogOwners can have many Dogs
    owner=relationship("DogOwner", back_populates="dogs")

    # Also, a Dog can have many Woofs.
    woofs= relationship("Woof", back_populates="dog")


