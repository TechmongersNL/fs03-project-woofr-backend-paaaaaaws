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

@app.get("/")
async def root():
    return {"message": "Woof!"}

@app.post("/woofs", response_model=schemas.Woof)
def post_woof(woof: schemas.WoofCreate, db: Session = Depends(get_db)):
    return woofs.create_woof(db, woof=woof)