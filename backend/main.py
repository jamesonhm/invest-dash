import logging
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from . import db
from backend.scraper import scrape

logger = logging.getLogger(__name__)
app = FastAPI()


@app.on_event("startup")
def startup():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scrape, CronTrigger.from_crontab('0 21 * * 1-5'))
    scheduler.start()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/tickers")
def get_tickers(limit: int = 30):
    result = db.get_ticker_eods()
    print(result)
    return result

@app.get("/ticker/{symbol}")
def get_ticker(symbol: str):
    result = db.get_ticker(symbol)
    return result