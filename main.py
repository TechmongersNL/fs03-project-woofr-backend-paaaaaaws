from typing import List
from fastapi import FastAPI, Depends, HTTPException
from dotenv import load_dotenv
from woofs import schemas, woofs
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

#To-Do
# POST /woofs – to create a Woof
# DELETE /woofs/{id} – to delete a Woof
# GET /woofs – for the feed, so orderable by created_at, desc.


@app.post("/woofs", response_model=schemas.Woof)
def post_woof(woof: schemas.WoofCreate, db: Session = Depends(get_db)):
    return woofs.create_woof(db, woof=woof)

@app.delete("/woofs{id}", response_model=schemas.Woof)
def delete_woof_by_id(woof_id: int, db: Session = Depends(get_db)):
    results = woofs.delete_woof(db, woof_id=woof_id)
    if results is None:
        raise HTTPException(status_code=404, detail="Woof not found")
    return results

@app.get("/woofs", response_model=list[schemas.Woof])
def fetch_woofs(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    results = woofs.get_woofs(db, skip=skip, limit=limit)
    if results is None:
        raise HTTPException(status_code=404, detail="No woofs found")
    return results
