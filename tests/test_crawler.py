from bs4 import BeautifulSoup
import requests
import pytest

from ..crawler.site_ifaces import CrawlSite, crawlsites

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; \
    Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/84.0.4147.105 Safari/537.36'}

SYMBOL = "NKE"
pages = [requests.get(crawlsite.get_url(SYMBOL), headers=headers) for crawlsite in crawlsites]
resp_args = [(crawlsite, "NKE") for crawlsite in crawlsites]


# @pytest.mark.parametrize("crawlsite, symbol", resp_args)
# def test_response(crawlsite: CrawlSite, symbol: str) -> None:
#     page = requests.get(crawlsite.get_url(symbol), headers=headers)
#     assert page.status_code == 200

@pytest.mark.parametrize("page", pages)
def test_response(page: requests.Response) -> None:
    assert page.status_code == 200

close_args = [(crawlsite, BeautifulSoup(page.text, 'html.parser'), 107.39) for crawlsite, page in zip(crawlsites, pages)]

@pytest.mark.parametrize("crawlsite, soup, static_close", close_args)
def test_prev_close(crawlsite: CrawlSite, soup: BeautifulSoup, static_close: float) -> None:
    close = crawlsite.get_close(soup)
    assert close == static_close