from datetime import datetime
import logging
from operator import itemgetter
import polars as pl
import random
import time

from backend.db import get_ticker, get_ticker_latest, update_history, update_history_many
from backend.yfi import get_days_history

MIN_DAYS = 10
MAX_DAYS = 90
TICKERS = ["AAPL", "MSFT", "AMZN", "TSLA", "GOOGL", "GOOG", "META", "NVDA", "UNH", "JNJ"]
EMA_WINDOW = 3
ROC_WINDOW = 3

logger = logging.getLogger('apscheduler')
test_logger = logging.getLogger(__name__)

def update():
    """ 
    iterate tickers and get close data from api
    """

    for ticker in TICKERS:
        # calc days worth of data to query based on what is saved in db
        query_days = calc_query_days(ticker)
        logger.info(f"this is from the apscheduler logger, {query_days} days needed for {ticker}")
        if query_days < 1:
            continue
                
        new_data = get_days_history(ticker, query_days)
        update_history_many(new_data)
        
        # calc sroc for ticker and update sroc table
        ts, sroc = calc_sroc(ticker)
        update_ticker_sroc(ticker, ts, sroc)

        # prune data

        sleep_time = random.randrange(1, 10)
        print(f"sleep: {sleep_time}", flush=True)
        time.sleep(sleep_time)


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


def calc_sroc(ticker: str, ema_window: int = EMA_WINDOW, roc_window: int = ROC_WINDOW) -> float:
    result = get_ticker(ticker)
    headers = ["timestamp", "close"]
    data_series = [[row["timestamp"] for row in result], [row["close"] for row in result]]
    dict_data = {header: data for header, data in zip(headers, data_series)}
    df = pl.from_dict(dict_data)
    print(df)
    df = df.with_columns(df["close"].ewm_mean(span=ema_window).alias("ema"))
    print(df)
    df = df.with_columns((100.0 * (df["ema"] / df["ema"].shift(roc_window) - 1.0)).alias("sroc"))
    print(df)
    return (df["timestamp"][-1], df["sroc"][-1])


if __name__ == "__main__":
    # print(calc_ema('AMZN'))
    update()
