from datetime import datetime
import logging
from operator import itemgetter
import polars as pl
import random
import time

from backend.db import get_ticker, get_ticker_latest, update_history, update_history_many
from backend.yfi import get_days_history

MIN_DAYS = 10
TICKERS = ["AAPL", "MSFT", "AMZN", "TSLA", "GOOGL", "GOOG", "META", "NVDA", "UNH", "JNJ"]
EMA_WINDOW = 3
ROC_WINDOW = 3

logger = logging.getLogger('apscheduler')
test_logger = logging.getLogger(__name__)


def calc_ema(ticker: str, ema_window: int = EMA_WINDOW, roc_window: int = ROC_WINDOW) -> float:
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


def update():
    """ 
    iterate tickers and get close data from api
    """

    for ticker in TICKERS:
        # check current data count and latest ts
        latest_data = get_ticker_latest(ticker)[0]
        latest, daycount = latest_data['latest'], latest_data['daycount']

        print(f"{ticker}: latest: {latest}, daycount: {daycount}", flush=True)
        
        if latest is None:
            query_days = MIN_DAYS
            print(f"no data, query days = {query_days}", flush=True)
        else:  
            days_since_latest = int((datetime.now().timestamp() - latest)/86400)
            print(f"days_since: {days_since_latest}", flush=True)
            if days_since_latest + daycount < MIN_DAYS or days_since_latest > MIN_DAYS: 
                query_days = MIN_DAYS
                print(f"not enough data, days_since = {days_since_latest}, daycount = {daycount}, query days = {query_days}", flush=True)
            elif days_since_latest == 0:
                print("Zero days, continuing", flush=True)
                continue
            else:
                query_days = days_since_latest
                print(f"close data, query days = {query_days}", flush=True)
                
        new_data = get_days_history(ticker, query_days)
        update_history_many(new_data)
        
        # calc sroc for ticker and update sroc table
        ts, sroc = calc_ema(ticker)


        sleep_time = random.randrange(1, 10)
        print(f"sleep: {sleep_time}", flush=True)
        time.sleep(sleep_time)

if __name__ == "__main__":
    # print(calc_ema('AMZN'))
    update()
