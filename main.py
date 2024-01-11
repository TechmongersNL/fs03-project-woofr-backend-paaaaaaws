from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Woof!"}
