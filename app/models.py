from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
import sys
import os
import datetime

# Routing to the app directory
path = os.path.abspath("app")
sys.path.append(path)

from app.database import Base

class Woof(Base):
    __tablename__ = "woofs"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    message = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


