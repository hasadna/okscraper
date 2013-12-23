from base import ParsingFromFileTestCase
from tests.lobbyists.lobbyist import LobbyistScraper

class testLobbyistScraper(ParsingFromFileTestCase):

    def _getScraperClass(self):
        return LobbyistScraper

    def _getFilename(self):
        return 'View_lobbyist_<<id>>.xml'

    def _getScrapeArgs(self):
        return [220]

    def _getExpectedData(self):
        return {
            'corporation_id': u'',
            'corporation_name': u'',
            'faction_member': u'\u05dc\u05d0',
            'faction_name': u'',
            'family_name': u'\u05d0\u05d1\u05d9\u05d6\u05d5\u05d4\u05e8',
            'first_name': u'\u05d9\u05d5\u05ea\u05dd',
            'id': u'220',
            'permit_type': u'\u05e7\u05d1\u05d5\u05e2',
            'profession': u''
        }
