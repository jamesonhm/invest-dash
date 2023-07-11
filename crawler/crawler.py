import requests
from bs4 import BeautifulSoup

from site_ifaces import CrawlSite


headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; \
    Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/84.0.4147.105 Safari/537.36'}

url = "https://finance.yahoo.com/quote/nke"
page = requests.get(url, headers=headers)

print(page.status_code)

soup = BeautifulSoup(page.text, 'html.parser')

close_price = soup.find("fin-streamer", {"class":"Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text
# volume = soup.find_all("fin-streamer")#, {"class":"Ta(end) Fw(600) Lh(14px)"}).text
volume = soup.find("fin-streamer", {"data-field": "regularMarketVolume"}).text#, {"class":"Ta(end) Fw(600) Lh(14px)"}).text

print(close_price)
print(volume)

test = CrawlSite("https://finance.yahoo.com/quote/{}", "fin-streamer", {"class":"Fw(b) Fz(36px) Mb(-4px) D(ib)"})
print(test.get_url("nke"))

