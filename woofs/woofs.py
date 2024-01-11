from sqlalchemy.orm import Session
from . import  schemas
from app import models

#get woofs
def get_woofs(db: Session, skip: int = 0, limit: int = 20):
    woofs = db.query(models.Woof).offset(skip).limit(limit).all()
    print(woofs)
    return woofs

#create woof
def create_woof(db: Session, woof: schemas.Woof):
    db_woof = models.Woof(**woof.dict())
    db.add(db_woof)
    db.commit()
    db.refresh(db_woof)
    return db_woof

#delete woof 
def delete_woof(db: Session, woof_id: int):
    woof = db.query(models.Woof).filter(models.Woof.id == woof_id).first()
    db.delete(woof)
    db.commit()
    return woof