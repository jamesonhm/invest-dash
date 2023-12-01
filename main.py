from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2_fragments.fastapi import Jinja2Blocks
import logging
from pathlib import Path

from backend import db
from backend.helpers import from_json, ts_to_str, score_round
from backend.updater import update

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Blocks(directory=str(BASE_PATH / "frontend/templates"))
templates.env.filters["from_json"] = from_json

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(year='*', month='*', day='*',
                          day_of_week='mon-fri', hour='22',
                          minute='55', timezone="US/Mountain")
    scheduler.add_job(update, trigger=trigger, name="Updater")
    scheduler.start()
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)




@app.get("/", status_code=200, response_class=HTMLResponse)
def root(request: Request, limit: int = 10):
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
    context = {"request": request,
               "ticker": ticker,
               "labels": labels,
               "y1": closes,
               "y2": scores,
               "ts_to_str": ts_to_str}
    block_name = None
    # if request.headers.get("HX-Request"):
    #     block_name = "chart"
    return templates.TemplateResponse("chart.html",
                                      context,
                                      block_name=block_name)


@app.get("/chart_data2", status_code=200, response_class=HTMLResponse)
def chart_data2(request: Request, ticker: str = ''):
    data = db.get_ticker_sroc(ticker)
    # data = json.dumps(data)
    context = {"request": request,
               "data": data}
    return templates.TemplateResponse("chart2.html",
                                      context)


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


