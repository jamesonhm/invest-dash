from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from jinja2_fragments.fastapi import Jinja2Blocks
import logging
from markupsafe import Markup
from pathlib import Path

from backend import db
from backend.helpers import ts_to_str, score_round
from backend.updater import update

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Blocks(directory=str(BASE_PATH / "frontend/templates"))
templates.env.filters["ts_to_str"] = ts_to_str

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
def startup():
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(year='*', month='*', day='*',
                          day_of_week='mon-fri', hour='17',
                          minute='55', timezone="US/Mountain")
    scheduler.add_job(update, trigger=trigger, name="Updater")
    scheduler.start()


@app.get("/", status_code=200, response_class=HTMLResponse)
def root(request: Request, limit: int = 20):
    data = db.get_latest_scores(limit)
    context = {"request": request,
               "data": data,
               "ts_to_str": ts_to_str,
               "round": score_round}
    block_name = None
    if request.headers.get("HX-Request"):
        block_name = "table"
    return templates.TemplateResponse("index.html",
                                      context,
                                      block_name=block_name)


@app.get("/chart_data", status_code=200, response_class=HTMLResponse)
def chart_data(request: Request, ticker: str = ''):
    data = db.get_history(ticker)
    # print(f"request: {request.json()}")
    print(f"ticker: {ticker}")
    # labels = [Markup(ts_to_str(row["timestamp"])) for row in data]
    labels = [row["timestamp"] for row in data]
    closes = [round(row["close"] or 0, 2) for row in data]
    scores = [round(row["sroc"] or 0, 2) for row in data]
    chart_data = {"labels": labels,
                  "y1": closes,
                  "y2": scores}
    context = {"request": request,
               "labels": labels,
               "y1": closes,
               "y2": scores,
               "ts_to_str": ts_to_str}
    block_name = None
    if request.headers.get("HX-Request"):
        block_name = "chart"
    return templates.TemplateResponse("chart.html",
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


