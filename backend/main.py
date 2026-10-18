
from fastapi import FastAPI

app = FastAPI(title="Auction API")


@app.get("/")
def home():
    return {"message": "Auction API is running"}
