from bs4 import BeautifulSoup
import requests
import pytest

from ..crawler.scrapesites import ScrapeSite, scrapesites

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; \
    Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/84.0.4147.105 Safari/537.36'}

SYMBOL = "NKE"
pages = [requests.get(scrapesite.get_url(SYMBOL), headers=headers) for scrapesite in scrapesites]
resp_args = [(scrapesite, "NKE") for scrapesite in scrapesites]


# @pytest.mark.parametrize("scrapesite, symbol", resp_args)
# def test_response(scrapesite: CrawlSite, symbol: str) -> None:
#     page = requests.get(scrapesite.get_url(symbol), headers=headers)
#     assert page.status_code == 200

@pytest.mark.parametrize("page", pages)
def test_response(page: requests.Response) -> None:
    assert page.status_code == 200

close_args = [(scrapesite, BeautifulSoup(page.text, 'html.parser'), 107.39) for scrapesite, page in zip(scrapesites, pages)]

@pytest.mark.parametrize("scrapesite, soup, static_close", close_args)
def test_prev_close(scrapesite: ScrapeSite, soup: BeautifulSoup, static_close: float) -> None:
    close = scrapesite.get_close(soup)
    assert close == static_close