from base import Scraper
from util import url

class LobbyistsScraper(Scraper):

    class Meta:
        html_parser = 'BeautifulSoup'

    urls = {
        'index': 'http://knesset.gov.il/',
        'lobbyist': url('http://knesset.gov.il/lobbyist/{{id}}'),
        'lobbyist_represent': url('http://knesset.gov.il/lobbyist/{{id}}/represent')
    }

    def _getLobbyistIdsFromSoup(self, soup):
        return [1,2,3]

    def _getLobbyistDataFromSoup(self, soup):
        return {}

    def _getLobbyistRepresentDataFromSoup(self, soup):
        return [4,5,6]

    def main(self):
        soup = self._fetchHtml('index')
        lobbyist_ids = self._getLobbyistIdsFromSoup(soup)
        for lobbyist_id in lobbyist_ids:
            lobbyist_data = self._getLobbyistDataFromSoup(
                self._fetchHtml('lobbyist', lobbyist_id)
            )
            lobbyist_data['represent'] = self._getLobbyistRepresentDataFromSoup(
                self._fetchHtml('lobbyist_represent', lobbyist_id)
            )

