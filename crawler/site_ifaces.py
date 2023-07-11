from abc import ABC, abstractmethod
from dataclasses import dataclass


# https://finance.yahoo.com/quote/nke
# https://digital.fidelity.com/prgw/digital/research/quote/dashboard/summary?symbol=NKE
# https://www.investopedia.com/markets/quote?tvwidgetsymbol=NKE
# https://www.bloomberg.com/quote/NKE:US
# https://www.marketwatch.com/investing/stock/nke
# https://www.morningstar.com/stocks/xnys/nke/quote
# https://seekingalpha.com/symbol/NKE
# https://www.zacks.com/stock/quote/NKE
# https://www.tradingview.com/chart/?symbol=NKE
# https://finviz.com/quote.ashx?t=NKE&p=d


@dataclass
class CrawlSite:
    url_fstr: str
    close_tag: str
    close_attrs: dict
    vol_tag: str
    vol_attrs: dict

    def get_url(self, symbol: str) -> str:
        return self.url_fstr.format(symbol)

yahoo = CrawlSite("https://finance.yahoo.com/quote/{}",
                  "fin-streamer", 
                  {"class":"Fw(b) Fz(36px) Mb(-4px) D(ib)"},
                  "fin-streamer", 
                  {"data-field": "regularMarketVolume"})

crawlsites= [yahoo]