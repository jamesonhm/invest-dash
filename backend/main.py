from fastapi import FastAPI

from . import db

app = FastAPI()

# test comm

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/tickers")
def get_tickers(limit: int = 30):
    with db.con as con:
        result = con.execute(f"""
        SELECT 
            date, 
            ticker, 
            close
        FROM 
            ticker_eod
        """).fetchall()
        print(result)
        return result

@app.get("/tickers2")
def get_tickers(limit: int = 30):
    result = db.get_ticker_eods2()
    print(result)
    return result