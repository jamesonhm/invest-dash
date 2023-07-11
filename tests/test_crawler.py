import sys
sys.path.append("..")

import requests
import pytest

from crawler.site_ifaces import crawlsites

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; \
    Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/84.0.4147.105 Safari/537.36'}

symbols = ["NKE"]

args = [(crawlsite, "NKE") for crawlsite in crawlsites]
@pytest.mark.parametrize("crawlsite, symbol", args)
def test_response(crawlsite, symbol):
    page = requests.get(crawlsite.get_url(symbol), headers=headers)
    assert page.status_code == 200