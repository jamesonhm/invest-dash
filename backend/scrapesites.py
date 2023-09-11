from bs4 import BeautifulSoup

### TODO: update for eoddata to read prices from tables
# https://eoddata.com/symbols.aspx


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


class ScrapeSite_Yahoo():
    def __init__(self):
        self.__url_fstr = "https://finance.yahoo.com/quote/{}"

    def get_url(self, symbol: str) -> str:
        return self.__url_fstr.format(symbol)

    def get_close(self, soup: BeautifulSoup) -> float:
        close = soup.find("fin-streamer", {"class":"Fw(b) Fz(36px) Mb(-4px) D(ib)", "data-test":"qsp-price"}).text
        try:
            return float(close)
        except:
            return 0.0

