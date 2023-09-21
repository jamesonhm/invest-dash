from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI
import logging

from . import db
from backend.crontest import crontest
from backend.updater import update

logger = logging.getLogger(__name__)
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)
app = FastAPI()


@app.on_event("startup")
def startup():
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(year='*', month='*', day='*', day_of_week='mon-fri', hour='21', minute='0', timezone="US/Eastern")

    trigger2 = CronTrigger(year='*', month='*', day='*', day_of_week='mon-fri', hour='18', minute='0', timezone="US/Eastern")
    scheduler.add_job(update, trigger=trigger2, name="Updater")
    scheduler.start()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/tickers")
def get_tickers(limit: int = 30):
    result = db.get_ticker_eods()
    # print(result)
    return result

@app.get("/tickers/{symbol}/close")
def get_ticker(symbol: str):
    result = db.get_ticker(symbol)
    return result

@app.get("/tickers/{symbol}/scores")
def get_ticker(symbol: str):
    result = db.get_ticker_sroc(symbol)
    return result

@app.get("/tickers/scores")
def get_ticker(symbol: str):
    result = db.get_latest_scores()
    return result