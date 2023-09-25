from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import logging
from pathlib import Path

from . import db
from backend.updater import update

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

app = FastAPI()
BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "../frontend/templates"))


@app.on_event("startup")
def startup():
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(year='*', month='*', day='*',
                          day_of_week='mon-fri', hour='18',
                          minute='0', timezone="US/Mountain")
    scheduler.add_job(update, trigger=trigger, name="Updater")
    scheduler.start()


@app.get("/", status_code=200, response_class=HTMLResponse)
def root(request: Request):
    data = db.get_latest_scores()
    return templates.TemplateResponse("index.html", {"request": request,
                                                     "data": data})


@app.get("/tickers")
def get_tickers():
    result = db.get_ticker_eods()
    return result


@app.get("/tickers/{symbol}/close")
def get_ticker(symbol: str):
    result = db.get_ticker(symbol)
    return result


@app.get("/tickers/{symbol}/scores")
def get_score(symbol: str):
    result = db.get_ticker_sroc(symbol)
    return result


@app.get("/tickers/scores", status_code=200)
def get_scores():
    data = db.get_latest_scores()
    return data
