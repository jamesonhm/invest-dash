import random
import time
import requests
from bs4 import BeautifulSoup

from scrapesites import scrapesites
symbols = ["AAPL", "MSFT", "AMZN", "TSLA", "GOOGL", "GOOG", "META", "NVDA", "UNH", "JNJ"]

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; \
    Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/84.0.4147.105 Safari/537.36'}

for symbol in symbols:
    # site = random.choice(scrapesites)
    site = scrapesites[0]
    url = site.get_url(symbol)
    print(url)
    page = requests.get(url, headers=headers)
    print(page.status_code)
    soup = BeautifulSoup(page.text, 'html.parser')
    close = site.get_close(soup)
    print(f"Close: {close}")
    sleep_time = random.randrange(1, 10)
    print(f"sleep: {sleep_time}")
    time.sleep(sleep_time)

    

# tag = soup.find("ul", {"class":"stock__quote-content stock__quote-content--overview"}).find_all('span')[2].text
# print(tag)
# for div in tag:
#     print(div)
# volume = soup.find_all("fin-streamer")#, {"class":"Ta(end) Fw(600) Lh(14px)"}).text
# volume = soup.find("fin-streamer", {"data-field": "regularMarketVolume"}).text#, {"class":"Ta(end) Fw(600) Lh(14px)"}).text

# print(close_price)
# print(volume)

# test = ScrapeSite("https://finance.yahoo.com/quote/{}", "fin-streamer", {"class":"Fw(b) Fz(36px) Mb(-4px) D(ib)"})
# print(test.get_url("nke"))

