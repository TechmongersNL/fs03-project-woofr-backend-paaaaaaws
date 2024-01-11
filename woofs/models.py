from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class Woof(Base):
    __tablename__ = "woofs"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    message = Column(String)
    created_at = Column(Datetime)


