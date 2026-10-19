from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.db import Base, engine
from config.settings import settings
from models import User, Game
from routers.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)


@app.get("/")
def home():
    return {"message": "Auction API is running"}