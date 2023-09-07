from bs4 import BeautifulSoup
import csv
from datetime import date
import random
import requests
import time

from backend.scrapesites import ScrapeSite_Yahoo
from backend.db import add_ticker_eod

tickers = ["AAPL", "MSFT", "AMZN", "TSLA", "GOOGL", "GOOG", "META", "NVDA", "UNH", "JNJ"]
# with open('/invest_dash/top_100_symbols.csv', newline='') as f:
#     reader = csv.reader(f)
#     tickers = [row[0] for row in reader]

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; \
    Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/84.0.4147.105 Safari/537.36'}

today = date.today()
yahoo = ScrapeSite_Yahoo()

def scrape():
    for ticker in tickers:
        # currently only works with yahoo
        url = yahoo.get_url(ticker)

        with requests.get(url, headers=headers) as page:
            if page.status_code != 200:
                print(f"{today}: request failed for page {url} with status code {page.status_code}")
                continue
            soup = BeautifulSoup(page.text, 'html.parser')
            close = yahoo.get_close(soup)
            if close <= 0.0:
                print(f"{today}: Bad close price found for {ticker}: {close}")
                continue
            print(f"{today}: Inserting EOD close for {ticker}, value: {close}")
            add_ticker_eod(today, ticker, close)
        
        sleep_time = random.randrange(1, 10)
        print(f"sleep: {sleep_time}")
        time.sleep(sleep_time)

if __name__ == "__main__":
    scrape()
    