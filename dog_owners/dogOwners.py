from sqlalchemy.orm import Session
from . import dogOwnersSchemas, authentication
from app import models


# for auth


# get_owner


def get_owner(db: Session, dog_owner_id: int):
    dog_owner = db.query(models.DogOwner).filter(
        models.DogOwner.id == dog_owner_id).first()
    print(dog_owner)
    return dog_owner

# get_owners


def get_owners(db: Session, skip: int = 0, limit: int = 20):
    owners = db.query(models.DogOwner).offset(skip).limit(limit).all()
    print(owners)
    return owners

# create_owner


def create_owner(db: Session, dog_owner: dogOwnersSchemas.DogOwnerCreate):
    password_hash = authentication.get_hashed_password(
        password=dog_owner.password)
    db_owner = models.DogOwner(
        email=dog_owner.email, password_hash=password_hash)
    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)
    return db_owner

# update owner username and about_me sections *Authenticated Request*


def update(db: Session, dog_owner_id: int, updated_data: dogOwnersSchemas.DogOwnerUpdate):
    existing_owner = db.query(models.DogOwner).filter(
        models.DogOwner.id == dog_owner_id)
    existing_owner.update(updated_data.dict(), synchronize_session=False)
    db.commit()
    return existing_owner.first()

# delete owner


def delete_owner(db: Session, dog_owner_id: int):
    owner = db.query(models.DogOwner).filter(
        models.DogOwner.id == dog_owner_id).first()
    db.delete(owner)
    db.commit()
    return owner
