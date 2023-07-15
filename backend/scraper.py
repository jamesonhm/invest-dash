import random
import time
import requests
from bs4 import BeautifulSoup
from datetime import date
import sqlite3

from scrapesites import scrapesites
from db import create_eod_table, add_ticker_eod

symbols = ["AAPL", "MSFT", "AMZN", "TSLA", "GOOGL", "GOOG", "META", "NVDA", "UNH", "JNJ"]

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; \
    Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/84.0.4147.105 Safari/537.36'}

today = date.today()
create_eod_table()

for symbol in symbols:
    # currently only works with yahoo
    site = scrapesites[0]
    url = site.get_url(symbol)

    page = requests.get(url, headers=headers)
    if page.status_code != 200:
        print(f"request failed for page {url} with status code {page.status_code}")
        continue
    soup = BeautifulSoup(page.text, 'html.parser')
    close = site.get_close(soup)
    print(f"Close: {close}")
    
    add_ticker_eod(today, symbol, close)
    sleep_time = random.randrange(1, 10)
    print(f"sleep: {sleep_time}")
    time.sleep(sleep_time)
