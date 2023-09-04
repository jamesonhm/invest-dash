import logging
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

from . import db
from . import crontest

logger = logging.getLogger(__name__)
app = FastAPI()


@app.on_event("startup")
def startup():
    scheduler = BackgroundScheduler()
    scheduler.add_job(crontest.main, 'cron', minute='*/1')
    scheduler.start()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/tickers")
def get_tickers(limit: int = 30):
    result = db.get_ticker_eods()
    print(result)
    return result

