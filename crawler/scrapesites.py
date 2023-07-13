from abc import ABC, abstractmethod
from dataclasses import dataclass
from bs4 import BeautifulSoup


# https://finance.yahoo.com/quote/nke
# X https://digital.fidelity.com/prgw/digital/research/quote/dashboard/summary?symbol=NKE
# https://www.investopedia.com/markets/quote?tvwidgetsymbol=NKE
# https://www.bloomberg.com/quote/NKE:US
# https://www.marketwatch.com/investing/stock/nke
# https://www.morningstar.com/stocks/xnys/nke/quote
# M https://seekingalpha.com/symbol/NKE
# M https://www.zacks.com/stock/quote/NKE
# https://www.tradingview.com/chart/?symbol=NKE
# https://finviz.com/quote.ashx?t=NKE&p=d


class ScrapeSite(ABC):
    def __init__(self, url_fstr: str):
        self.url_fstr = url_fstr
    
    @abstractmethod
    def get_url(self, symbol: str) -> str:
        pass
    
    @abstractmethod
    def get_close(self, soup: BeautifulSoup) -> float:
        pass


class ScrapeSite_Yahoo(ScrapeSite):

    def get_url(self, symbol: str) -> str:
        return self.url_fstr.format(symbol)
    
    def get_close(self, soup: BeautifulSoup) -> float:
        close = soup.find("fin-streamer", {"class":"Fw(b) Fz(36px) Mb(-4px) D(ib)", "data-test":"qsp-price"}).text
        try:
            return float(close)
        except:
            return 0.0


class ScrapeSite_Morningstar(ScrapeSite):

    def get_url(self, symbol: str) -> str:
        return self.url_fstr.format(symbol)
    
    def get_close(self, soup: BeautifulSoup) -> float:
        close = soup.find("ul", {"class":"stock__quote-content stock__quote-content--overview"}).find_all('span')[2].text
        try:
            return float(close)
        except:
            return 0.0

yahoo = ScrapeSite_Yahoo("https://finance.yahoo.com/quote/{}")

mstar = ScrapeSite_Morningstar("https://www.morningstar.com/stocks/xnys/{}/quote")

scrapesites= [yahoo, mstar]