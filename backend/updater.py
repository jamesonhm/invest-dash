from datetime import datetime

from backend import db #import get_ticker_latest, update_ticker_close
from backend import yfi

MIN_DAYS = 10
TICKERS = ["AAPL", "MSFT", "AMZN", "TSLA", "GOOGL", "GOOG", "META", "NVDA", "UNH", "JNJ"]

def update():
    """ 
    iterate tickers and get close data from api
    """

    for ticker in TICKERS:
        # check current data count and latest ts
        latest_count = db.get_ticker_latest(ticker)
        latest = latest_count[0]['latest']
        daycount = latest_count[0]['daycount']
        print(latest, daycount)
        
        if latest is None:
            query_days = MIN_DAYS
            print(f"no data, query days = {query_days}")
        else:  
            days_since_latest = int((datetime.now().timestamp() - latest)/86400)
            print(f"days_since: {days_since_latest}")
            if days_since_latest + daycount < MIN_DAYS or days_since_latest > MIN_DAYS: 
                query_days = MIN_DAYS
                print(f"not enough data, days_since = {days_since_latest}, daycount = {daycount}, query days = {query_days}")
            elif days_since_latest == 0:
                print("Zero days, continuing")
                continue
            else:
                query_days = days_since_latest
                print(f"close data, query days = {query_days}")
                
        new_data = yfi.get_days_history(ticker, query_days)
        for timestamp, close in new_data:
            db.update_history(ticker, timestamp, close)

if __name__ == "__main__":
    update()
