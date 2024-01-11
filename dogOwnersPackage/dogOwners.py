from sqlalchemy.orm import Session
from . import  dogOwnersSchemas
from app import models

#get_owner
def get_owner(db: Session, dog_owner_id: int):
    dog_owner = db.query(models.Dog_owner).filter(models.Dog_owner.id == dog_owner_id).first()
    print(dog_owner)
    return dog_owner

#get_owners
def get_owners(db: Session, skip: int = 0, limit: int = 20):
    owners = db.query(models.Dog_owner).offset(skip).limit(limit).all()
    print(owners)
    return owners

#create_owner
def create_owner(db: Session, owner: dogOwnersSchemas.DogOwnerCreate):
    db_owner = models.Dog_owner(**owner.dict())
    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)
    return db_owner  

#delete owner
def delete_owner(db: Session, dog_owner_id: int):
    owner = db.query(models.Dog_owner).filter(models.Dog_owner.id == dog_owner_id).first()
    db.delete(owner)
    db.commit()
    return owner