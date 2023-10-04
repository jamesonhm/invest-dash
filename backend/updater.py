import csv
from datetime import datetime
import logging
from pathlib import Path
import polars as pl
import random
import time

from backend.db import get_ticker, get_ticker_latest, update_close_many, update_sroc_many
from backend.yfi import get_days_history


BASE_PATH = Path(__file__).resolve().cwd()
TICKER_PATH = BASE_PATH / "top_100_symbols.csv"


MIN_DAYS = 20
MAX_DAYS = 90
# TICKER_PATH = "../top_100_symbols.csv"
# TICKERS = ["AAPL", "MSFT", "AMZN", "TSLA", "GOOGL", "GOOG", "META", "NVDA", "UNH", "JNJ", "V", "WMT", "PG", "JPM"]
with open(TICKER_PATH, 'r') as f:
    reader = csv.reader(f)
    TICKERS = [row[0] for row in reader]
EMA_WINDOW = 3
ROC_WINDOW = 3

logger = logging.getLogger('apscheduler')
test_logger = logging.getLogger(__name__)


def update():
    """
    iterate tickers and get close data from api
    """
    tickers = get_tickerslice(TICKERS)
    for ticker in tickers:
        # calc days worth of data to query based on what is saved in db
        query_days = calc_query_days(ticker)

        logger.info(f"this is from the apscheduler logger, {query_days} days needed for {ticker}")
        if query_days < 1:
            continue
        new_data = get_days_history(ticker, query_days)
        update_close_many(new_data)

        # calc sroc for ticker and update sroc table
        sroc_data = calc_sroc(ticker)
        update_sroc_many(sroc_data)

        # prune data

        sleep_time = random.randrange(1, 10)
        print(f"sleep: {sleep_time}", flush=True)
        time.sleep(sleep_time)


def get_tickerslice(all_tickers: list) -> list:
    # weekday(): mon=0, sun=6
    wkday = datetime.now().weekday()
    tkrs_per_day = round(len(all_tickers) / 5)
    sl_start = wkday * tkrs_per_day
    if wkday == 4:
        # friday just goes to the end
        return all_tickers[sl_start:]    
    sl_end = sl_start + tkrs_per_day
    return all_tickers[sl_start: sl_end]


def calc_query_days(ticker: str, min_days: int = MIN_DAYS) -> int:
    latest_data = get_ticker_latest(ticker)[0]
    latest, daycount = latest_data['latest'], latest_data['daycount']

    print(f"{ticker}: latest: {latest}, daycount: {daycount}", flush=True)

    if latest is None:
        query_days = min_days
        print(f"no data, query days = {query_days}", flush=True)
    else:
        days_since_latest = int((datetime.now().timestamp() - latest)/86400)
        print(f"days_since: {days_since_latest}", flush=True)
        if days_since_latest + daycount < min_days or days_since_latest > min_days: 
            query_days = min_days
            print(f"not enough data, days_since = {days_since_latest}, daycount = {daycount}, query days = {query_days}", flush=True)
        elif days_since_latest == 0:
            print("Zero days, continuing", flush=True)
            query_days = 0
        else:
            query_days = days_since_latest
            print(f"recent data, query days = {query_days}", flush=True)
    return query_days


def calc_sroc(ticker: str, ema_window: int = EMA_WINDOW, roc_window: int = ROC_WINDOW) -> list[dict]:
    result = get_ticker(ticker)
    headers = ["timestamp", "close"]
    data_series = [[row["timestamp"] for row in result], [row["close"] for row in result]]
    dict_data = {header: data for header, data in zip(headers, data_series)}
    df = pl.from_dict(dict_data)
    df = df.with_columns(df["close"].ewm_mean(span=ema_window).alias("ema"))
    df = df.with_columns((100.0 * (df["ema"] / df["ema"].shift(roc_window) - 1.0)).alias("sroc"))
    df = df.drop(["close", "ema"]).drop_nulls("sroc")
    tkr_ser = pl.Series("ticker", [ticker] * len(df))
    df = df.with_columns(tkr_ser)
    return df.to_dicts()
    # return (df["timestamp"][-1], df["sroc"][-1])


if __name__ == "__main__":
    # calc_sroc('AMZN')
    update()
    # print(BASE_PATH)
    # print(TICKERS)
    # print(get_tickerslice(TICKERS))

