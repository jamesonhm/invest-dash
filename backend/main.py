from fastapi import FastAPI

from . import db

app = FastAPI()

# test comm

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/tickers")
def get_tickers(limit: int = 30):
    result = db.get_ticker_eods()
    print(result)
    return result