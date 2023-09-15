from datetime import datetime, timezone, timedelta
import json
import requests
from typing import List, Tuple

_BASE_URL_ = 'https://query2.finance.yahoo.com'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def _daily_close_history(ticker:str, period:str=None, interval:str='1d', 
            start:str=None, end:str=None, timeout:int=10) -> List[Tuple[int, float]] | None:
    """
    Args:
        ticker(str): 
            stock symbol to get history for
        period `range`(str):
            Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            Either Use period parameter or use start and end
        interval(str): Default 1d
            Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        start(datetime.timestamp):
            Download start datetime, inclusive.
            Default is 1 year ago
            E.g. for start="2020-01-01", the first data point will be on "2020-01-01"
        end(datetime.timestamp):
            Download end datetime, exclusive.
            Default is now
            E.g. for end="2023-01-01", the last data point will be on "2022-12-31"
    """

    url = f"{_BASE_URL_}/v8/finance/chart/{ticker}"
    
    params = {"interval": interval}

    if period is None:
        # use start end dates
        if start is None:
            period1 = datetime.now(timezone.utc) - timedelta(days=365)
            period1 = int(period1.timestamp())
        else:
            period1 = start
        if end is None:
            period2 = int(datetime.today().timestamp())
        else:
            period2 = end
        params["period1"] = period1
        params["period2"] = period2
    else:
        params["range"] = period

    # Getting data from json
    response = requests.get(
        url=url,
        headers=HEADERS,
        params=params,
        timeout=timeout
    )

    if response.status_code != 200:
        print(f"request failed for ticker {ticker} with status code {response.status_code}")
        return None
    rj = response.json()

    try:
        timestamps = rj["chart"]["result"][0]["timestamp"]
    except KeyError:
        print(f'KeyError for timestamp at path `rj["chart"]["result"][0]["timestamp"]`: {json.dumps(rj, indent=2)}')
        return None
    try:
        closes = rj["chart"]["result"][0]["indicators"]["adjclose"][0]["adjclose"]
    except KeyError:
        print(f'KeyError for closes at path `rj["chart"]["result"][0]["indicators"]["adjclose"][0]["adjclose"]`: {json.dumps(rj, indent=2)}')
        return None

    return list(zip(timestamps, closes))

def get_days_history(ticker: str, days: int):
    if days > 0:
        days = str(days) + 'd'
    else: 
        return None
    data = _daily_close_history(ticker, period=days)
    return data

def main():

    data = _daily_close_history('amzn', '3d')
    # start = int(datetime(year=2023, month=9, day=1).timestamp())
    # end = int(datetime(year=2022, month=9, day=20).timestamp())
    # data = _daily_close_history('amzn', end=end)
    prevts = 1694698200
    ts = int(datetime.now().timestamp())
    print((ts - prevts) / 86400)
    
    for k in data:
        print(k)

if __name__ == "__main__":
    main()