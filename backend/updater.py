from datetime import datetime
import logging
import time

from backend import db #import get_ticker_latest, update_ticker_close
from backend import yfi

MIN_DAYS = 10
TICKERS = ["AAPL", "MSFT", "AMZN", "TSLA", "GOOGL", "GOOG", "META", "NVDA", "UNH", "JNJ"]

logger = logging.getLogger('apscheduler')


def update():
    """ 
    iterate tickers and get close data from api
    """

    for ticker in TICKERS:
        # check current data count and latest ts
        latest_count = db.get_ticker_latest(ticker)
        latest = latest_count[0]['latest']
        daycount = latest_count[0]['daycount']
        logger.info(f"{ticker}: latest: {latest}, daycount: {daycount}")
        
        if latest is None:
            query_days = MIN_DAYS
            logger.info(f"no data, query days = {query_days}")
        else:  
            days_since_latest = int((datetime.now().timestamp() - latest)/86400)
            logger.info(f"days_since: {days_since_latest}")
            if days_since_latest + daycount < MIN_DAYS or days_since_latest > MIN_DAYS: 
                query_days = MIN_DAYS
                logger.info(f"not enough data, days_since = {days_since_latest}, daycount = {daycount}, query days = {query_days}")
            elif days_since_latest == 0:
                logger.info("Zero days, continuing")
                continue
            else:
                query_days = days_since_latest
                logger.info(f"close data, query days = {query_days}")
                
        new_data = yfi.get_days_history(ticker, query_days)
        for timestamp, close in new_data:
            db.update_history(ticker, timestamp, close)
        
        sleep_time = random.randrange(1, 10)
        logger.info(f"sleep: {sleep_time}")
        time.sleep(sleep_time)

if __name__ == "__main__":
    update()
