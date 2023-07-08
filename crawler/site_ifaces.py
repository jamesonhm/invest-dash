from abc import ABC, abstractmethod
from dataclasses import dataclass


class CrawlSite(ABC):
    @abstractmethod
    def get_symbol_url(self, symbol: str) -> str:
        pass

    @abstractmethod
    def get_closeprice_tagname(self):
        pass

    @abstractmethod
    def get_closeprice_tagattrs(self):
        pass


################## OR ######################

class CrawlSite2:
    def __init__(self, url_fstr: str, close_tag: str, close_tagattr: dict, vol_tag: str, vol_tagattrs: dict):
        self.url_ftstr = url_fstr
        self.close_tag = close_tag
        ...

    
################# OR ############################

@dataclass
class CrawlSite3:
    url_fstr: str
    close_tag: str
    close_attrs: dict

    def get_url(self, symbol: str) -> str:
        return self.url_fstr.format(symbol)