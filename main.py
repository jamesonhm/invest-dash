from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2_fragments.fastapi import Jinja2Blocks
import logging
from pathlib import Path

from backend import db
from backend.helpers import ts_to_str
from backend.updater import update

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Blocks(directory=str(BASE_PATH / "frontend/templates"))


@app.on_event("startup")
def startup():
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(year='*', month='*', day='*',
                          day_of_week='mon-fri', hour='18',
                          minute='0', timezone="US/Mountain")
    scheduler.add_job(update, trigger=trigger, name="Updater")
    scheduler.start()


@app.get("/", status_code=200, response_class=HTMLResponse)
def root(request: Request, limit: int = 20):
    data = db.get_latest_scores(limit)
    context = {"request": request,
               "data": data,
               "ts_to_str": ts_to_str}
    block_name = None
    if request.headers.get("HX-Request"):
        block_name = "table"
    return templates.TemplateResponse("index.html",
                                      context,
                                      block_name=block_name)


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


@app.get("/chart", response_class=HTMLResponse)
def get_chart(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("chart.html", context)


