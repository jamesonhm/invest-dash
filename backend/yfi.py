import json
import requests

"""
period (range) : str
                Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                Either Use period parameter or use start and end
interval : str
                Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                Intraday data cannot extend last 60 days

"""
_BASE_URL_ = 'https://query2.finance.yahoo.com'


headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

period = '1d'
interval = '1d'

params = {"range": period,
            "interval": interval}

# Getting data from json
ticker = 'aapl'
url = f"{_BASE_URL_}/v8/finance/chart/{ticker}"
data = None

data = requests.get(
    url=url,
    headers=headers,
    params=params,
    timeout=30
)

print(json.dumps(data.json(), indent=2))