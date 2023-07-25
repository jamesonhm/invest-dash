import random
import time
import requests
from bs4 import BeautifulSoup
from datetime import date
import sqlite3

from scrapesites import scrapesites
from db import create_eod_table, add_ticker_eod

tickers = ["AAPL", "MSFT", "AMZN", "TSLA", "GOOGL", "GOOG", "META", "NVDA", "UNH", "JNJ"]

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; \
    Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/84.0.4147.105 Safari/537.36'}

today = date.today()
create_eod_table()

def scrape():
    for ticker in tickers:
        # currently only works with yahoo
        site = scrapesites[0]
        url = site.get_url(ticker)

        with requests.get(url, headers=headers) as page:
            if page.status_code != 200:
                print(f"{today}: request failed for page {url} with status code {page.status_code}")
                continue
            soup = BeautifulSoup(page.text, 'html.parser')
            close = site.get_close(soup)
            if close <= 0.0:
                print(f"{today}: Bad close price found for {ticker}: {close}")
                continue
            add_ticker_eod(today, ticker, close)
        
        sleep_time = random.randrange(1, 10)
        print(f"sleep: {sleep_time}")
        time.sleep(sleep_time)

if __name__ == "__main__":
    scrape()
    