from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import datetime
from fastapi import FastAPI
import logging

from . import db
from backend.crontest import crontest
from backend.scraper import scrape

logger = logging.getLogger(__name__)
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)
app = FastAPI()


@app.on_event("startup")
def startup():
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(year='*', month='*', day='*', day_of_week='mon-fri', hour='21', minute='0', timezone="US/Eastern")
    # scheduler.add_job(scrape, CronTrigger.from_crontab('0 21 * * 1-5'))
    scheduler.add_job(scrape, trigger=trigger, name="Scraper")
    scheduler.start()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/tickers")
def get_tickers(limit: int = 30):
    result = db.get_ticker_eods()
    # print(result)
    return result

@app.get("/tickers/{symbol}")
def get_ticker(symbol: str):
    result = db.get_ticker(symbol)
    return result