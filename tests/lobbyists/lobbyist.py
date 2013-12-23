from base import BaseScraper
from sources import UrlSource
from storages import DictStorage
from bs4 import BeautifulSoup

class LobbyistScraper(BaseScraper):

    source = UrlSource('http://online.knesset.gov.il/WsinternetSps/KnessetDataService/LobbyistData.svc/View_lobbyist(<<id>>)')
    storage = DictStorage()

    def _storeLobbyistDataFromSoup(self, soup):
        self.storage.store('id', soup.find('d:lobbyist_id').text.strip())
        self.storage.store('first_name', soup.find('d:first_name').text.strip())
        self.storage.store('family_name', soup.find('d:family_name').text.strip())
        self.storage.store('profession', soup.find('d:profession').text.strip())
        self.storage.store('corporation_name', soup.find('d:corporation_name').text.strip())
        self.storage.store('corporation_id', soup.find('d:corporation_id').text.strip())
        self.storage.store('faction_member', soup.find('d:faction_member').text.strip())
        self.storage.store('faction_name', soup.find('d:faction_name').text.strip())
        self.storage.store('permit_type', soup.find('d:lobyst_permit_type').text.strip())

    def _scrape(self, lobbyist_id):
        html = self.source.fetch(lobbyist_id)
        soup = BeautifulSoup(html)
        return self._storeLobbyistDataFromSoup(soup)
