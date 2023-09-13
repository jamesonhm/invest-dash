import json
import requests

_BASE_URL_ = 'https://query2.finance.yahoo.com'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def _daily_close_history(ticker:str, period:str=None, interval:str='1d', 
            start:str=None, end:str=None, timeout:int=10):
    """
    Args:
        ticker(str): 
            stock symbol to get history for
        period `range`(str):
            Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            Either Use period parameter or use start and end
        interval(str): Default 1d
            Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        start(str):
            Download start date string (YYYY-MM-DD) or _datetime, inclusive.
            Default is 1 years ago
            E.g. for start="2020-01-01", the first data point will be on "2020-01-01"
        end(str):
            Download end date string (YYYY-MM-DD) or _datetime, exclusive.
            Default is now
            E.g. for end="2023-01-01", the last data point will be on "2022-12-31"
    """

    url = f"{_BASE_URL_}/v8/finance/chart/{ticker}"
    
    params = {"range": period,
            "interval": interval}

    # Getting data from json
    response = requests.get(
        url=url,
        headers=HEADERS,
        params=params,
        timeout=timeout
    )

    print(json.dumps(data.json(), indent=2))
    return data.json()
    
