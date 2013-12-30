from base import BaseScraper
from sources import UrlSource
from storages import ListStorage
from bs4 import BeautifulSoup

class LobbyistsIndexScraper(BaseScraper):

    def __init__(self):
        self.source = UrlSource('http://www.knesset.gov.il/lobbyist/heb/lobbyist.aspx')
        self.storage = ListStorage()

    def _storeLobbyistIdsFromSoup(self, soup):
        elts = soup.findAll(lobbyist_id=True)
        for elt in elts:
            lobbyist_id = elt.get('lobbyist_id')
            if lobbyist_id.isdigit():
                self.storage.store(lobbyist_id)

    def _scrape(self):
        html = self.source.fetch()
        soup = BeautifulSoup(html)
        return self._storeLobbyistIdsFromSoup(soup)
