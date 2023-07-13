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


@dataclass
class ScrapeSite:
    url_fstr: str
    close_tag: str
    close_attrs: dict
    # vol_tag: str
    # vol_attrs: dict

    def get_url(self, symbol: str) -> str:
        return self.url_fstr.format(symbol)
    
    def get_close(self, soup: BeautifulSoup) -> float:
        close = soup.find(self.close_tag, self.close_attrs).text
        try:
            return float(close)
        except:
            return 0.0

yahoo = ScrapeSite("https://finance.yahoo.com/quote/{}",
                  "td", 
                  {"class":"Ta(end) Fw(600) Lh(14px)", "data-test":"PREV_CLOSE-value"}, 
                )

mstar = ScrapeSite("https://www.morningstar.com/stocks/xnys/{}/quote",
                "span", 
                {"class": "mdc-data-point mdc-data-point--number"},
                )

scrapesites= [yahoo, mstar]