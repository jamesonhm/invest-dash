from fastapi import FastAPI

from .db import get_ticker_eods

app = FastAPI()

# test comm

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/tickers")
def get_tickers(limit: int = 30):
    tickers = get_ticker_eods()
    return tickers