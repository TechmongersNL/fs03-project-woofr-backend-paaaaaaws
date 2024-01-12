from typing import List
from fastapi import FastAPI, Depends, HTTPException
from dotenv import load_dotenv
from woofsPackage import woofsSchemas, woofs
from dogOwnersPackage import dogOwnersSchemas, dogOwners
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app import database, models

load_dotenv()  # take environment variables from .env.

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Middleware

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# DB Dependency


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# WOOFS ENDPOINTS
# POST /woofs – to create a Woof


@app.post("/woofs", response_model=woofsSchemas.Woof)
def post_woof(woof: woofsSchemas.WoofCreate, db: Session = Depends(get_db)):
    return woofs.create_woof(db, woof=woof)

# DELETE /woofs/{id} – to delete a Woof


@app.delete("/woofs{id}", response_model=woofsSchemas.Woof)
def delete_woof_by_id(woof_id: int, db: Session = Depends(get_db)):
    results = woofs.delete_woof(db, woof_id=woof_id)
    if results is None:
        raise HTTPException(status_code=404, detail="Woof not found")
    return results


# GET /woofs – for the feed, so orderable by created_at, desc.

@app.get("/woofs", response_model=list[woofs.woofsSchemas.Woof])
def fetch_woofs(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    results = woofs.get_woofs(db, skip=skip, limit=limit)
    if results is None:
        return []
    return results


# Dog Owner Endpoints

# GET /owners - get a list of all owners
@app.get("/owners", response_model=list[dogOwnersSchemas.DogOwnerBase])
def fetch_owners(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    results = dogOwners.get_owners(db, skip=skip, limit=limit)
    if results is None:
        return []
    return results

# GET /owners/{id} - get an owner by id


@app.get("/owners/{id}", response_model=dogOwnersSchemas.DogOwnerBase)
def get_owner_by_id(dog_owner_id: int, db: Session = Depends(get_db)):
    result = dogOwners.get_owner(db, dog_owner_id=dog_owner_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    return result


# POST /owners - create an owner on signup. Email address is a unique value


@app.post("/owners", response_model=dogOwnersSchemas.DogOwnerMe)
def create_an_owner(dog_owner: dogOwnersSchemas.DogOwnerCreate, db: Session = Depends(get_db)):
    try:
        result = dogOwners.create_owner(db, dog_owner=dog_owner)
    except:
        raise HTTPException(
            status_code=400, detail="Please use a different email and/or password")
    return result


# DELETE /owners/{id} - delete an owner by id
@app.delete("/owners/{id}", response_model=dogOwnersSchemas.DogOwnerBase)
def delete_owner_by_id(dog_owner_id: int, db: Session = Depends(get_db)):
    result = dogOwners.delete_owner(db, dog_owner_id=dog_owner_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    return result

# PUT /owners/{id} - update the username and about me details for an owner by an id


@app.put("/owners/{id}", response_model=dogOwnersSchemas.DogOwnerUpdate)
def update_owner(dog_owner_id: int, updated_data: dogOwnersSchemas.DogOwnerUpdate, db: Session = Depends(get_db)):
    existing_owner = db.query(models.Dog_owner).filter(
        models.Dog_owner.id == dog_owner_id).first()

    if not existing_owner:
        raise HTTPException(status_code=404, detail="Owner not found")

    for key, value in updated_data.dict().items():
        setattr(existing_owner, key, value)

    db.commit()
    db.refresh(existing_owner)

    return existing_owner
