from fastapi import FastAPI

from config.db import Base, engine
from models import User
from routers.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auction API")

app.include_router(auth_router)


@app.get("/")
def home():
    return {"message": "Auction API is running"}