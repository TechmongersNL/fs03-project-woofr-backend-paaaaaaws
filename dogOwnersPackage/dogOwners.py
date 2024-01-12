from sqlalchemy.orm import Session
from . import dogOwnersSchemas, authentication
from app import models


# for auth


# get_owner


def get_owner(db: Session, dog_owner_id: int):
    dog_owner = db.query(models.Dog_owner).filter(
        models.Dog_owner.id == dog_owner_id).first()
    print(dog_owner)
    return dog_owner

# get_owners


def get_owners(db: Session, skip: int = 0, limit: int = 20):
    owners = db.query(models.Dog_owner).offset(skip).limit(limit).all()
    print(owners)
    return owners

# create_owner


def create_owner(db: Session, dog_owner: dogOwnersSchemas.DogOwnerCreate):
    password_hash = authentication.get_hashed_password(
        password=dog_owner.password)
    db_owner = models.Dog_owner(
        email=dog_owner.email, password_hash=password_hash)
    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)
    return db_owner

# update owner username and about_me sections


def update(db: Session, dog_owner_id: int, updated_data: dogOwnersSchemas.DogOwnerUpdate):
    existing_owner = db.query(models.Dog_owner).filter(
        models.Dog_owner.id == dog_owner_id).first()

    if existing_owner:
        for key, value in updated_data.dict().items():
            setattr(existing_owner, key, value)

        db.commit()
        db.refresh(existing_owner)

    return existing_owner

# delete owner


def delete_owner(db: Session, dog_owner_id: int):
    owner = db.query(models.Dog_owner).filter(
        models.Dog_owner.id == dog_owner_id).first()
    db.delete(owner)
    db.commit()
    return owner
