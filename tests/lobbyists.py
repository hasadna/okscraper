# encoding: utf-8

import os
from base import Scraper, ScraperTestCase
from sources import UrlSource, FileSource
from storages import DictStorage
from bs4 import BeautifulSoup

class LobbyistsScraper(Scraper):

    sources = {
        'index': UrlSource('http://www.knesset.gov.il/lobbyist/heb/lobbyist.aspx'),
        'lobbyist': UrlSource('http://online.knesset.gov.il/WsinternetSps/KnessetDataService/LobbyistData.svc/View_lobbyist(<<id>>)'),
        'lobbyist_represent': UrlSource('http://online.knesset.gov.il/WsinternetSps/KnessetDataService/LobbyistData.svc/View_lobbyist(<<id>>)/lobbist_type'),
    }
    storages = {
        'lobbyist': DictStorage()
    }

    def _getLobbyistIdsFromSoup(self, soup):
        elts = soup.findAll(lobbyist_id=True)
        lobbyist_ids = []
        for elt in elts:
            lobbyist_id = elt.get('lobbyist_id')
            if lobbyist_id.isdigit():
                lobbyist_ids.append(int(lobbyist_id))
        return lobbyist_ids

    def _getLobbyistDataFromSoup(self, soup):
        data = {}
        data['id'] = soup.find('d:lobbyist_id').text.strip()
        data['first_name'] = soup.find('d:first_name').text.strip()
        data['family_name'] = soup.find('d:family_name').text.strip()
        data['profession'] = soup.find('d:profession').text.strip()
        data['corporation_name'] = soup.find('d:corporation_name').text.strip()
        data['corporation_id'] = soup.find('d:corporation_id').text.strip()
        data['faction_member'] = soup.find('d:faction_member').text.strip()
        data['faction_name'] = soup.find('d:faction_name').text.strip()
        data['permit_type'] = soup.find('d:lobyst_permit_type').text.strip()
        return data


    def _getLobbyistRepresentDataFromSoup(self, soup):
        data = []
        for elt in soup.findAll('content'):
            represent = {}
            represent['id'] = elt.find('d:lobbyist_represent_id').text.strip()
            represent['lobbyist_id'] = elt.find('d:lobbyist_id').text.strip()
            represent['name'] = elt.find('d:lobbyist_represent_name').text.strip()
            represent['domain'] = elt.find('d:lobbyist_represent_domain').text.strip()
            represent['type'] = elt.find('d:lobbyist_represent_type').text.strip()
            data.append(represent)
        return data

    def _storeLobbyistData(self, data):
        # store the data in DB..
        pass

    def storeAllLobbyistsData(self):
        lobbyist_ids = self.getAllLobbyistIds()
        for lobbyist_id in lobbyist_ids:
            lobbyist_data = self.getLobbyistData(lobbyist_id)
            self._store('lobbyist', lobbyist_id, lobbyist_data)

    def getAllLobbyistIds(self):
        html = self._fetch('index')
        soup = BeautifulSoup(html)
        return self._getLobbyistIdsFromSoup(soup)

    def getLobbyistData(self, lobbyist_id):
        xml = self._fetch('lobbyist', lobbyist_id)
        soup = BeautifulSoup(xml)
        data = self._getLobbyistDataFromSoup(soup)
        xml = self._fetch('lobbyist_represent', lobbyist_id)
        soup = BeautifulSoup(xml)
        data['represent'] = self._getLobbyistRepresentDataFromSoup(soup)
        return data

class testLobbyistScraper(ScraperTestCase):

    maxDiff = None
    DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
    lobbyist_220_data = {
            'corporation_name': u'',
            'family_name': u'אביזוהר',
            'first_name': u'יותם',
            'faction_name': u'',
            'represent': [
                {
                    'domain': u'איכות הסביבה, בריאות הציבור, בטיחות בדרכים',
                    'type': u'קבוע',
                    'id': u'6954817',
                    'name': u'ישראל בשביל אופניים',
                    'lobbyist_id': u'220'
                }, {
                    'domain': u'תחבורה, התחדשות עירונית, בטיחות בדרכים',
                    'type': u'קבוע',
                    'id': u'6954818',
                    'name': u'אופנים בשביל ירושלים',
                    'lobbyist_id': u'220'
                }
            ],
            'corporation_id': u'',
            'profession': u'',
            'permit_type': u'קבוע',
            'faction_member': u'לא',
            'id': u'220'
        }

    def testGetAllLobbyistIds(self):
        scraper = LobbyistsScraper()
        scraper.sources['index'] = FileSource(os.path.join(self.DATA_DIR, 'lobbyists_index.html'))
        self.assertListEqual(scraper.getAllLobbyistIds(), [220, 561, 405, 544, 221, 426, 450, 564, 309, 266, 547, 282, 299, 225, 269, 393, 548, 205, 429, 302, 572, 293, 228, 472, 395, 573, 515, 289, 231, 457, 232, 569, 347, 213, 214, 576, 234, 513, 430, 206, 545, 303, 451, 348, 324, 425, 489, 578, 456, 236, 452, 270, 238, 571, 376, 239, 312, 567, 240, 378, 300, 241, 399, 516, 242, 243, 424, 541, 245, 323, 246, 247, 446, 420, 325, 291, 568, 458, 540, 250, 557, 283, 209, 556, 570, 252, 539, 428, 286, 401, 566, 349, 253, 384, 379, 254, 579, 552, 437, 255, 388, 256, 377, 162, 558, 202, 352, 257, 543, 397, 292, 259, 298, 553, 400, 350, 261, 262, 306, 263, 212, 264, 432, 265, 326, 272, 460, 449, 332, 560, 546, 559, 555, 565, 520, 577, 549, 554, 551, 575, 563, 310])

    def testGetLobbyistData(self):
        scraper = LobbyistsScraper()
        scraper.sources = {
            'lobbyist': FileSource(os.path.join(self.DATA_DIR, 'View_lobbyist_<<id>>.xml')),
            'lobbyist_represent':  FileSource(os.path.join(self.DATA_DIR, 'lobbist_type_<<id>>.xml')),
        }
        data = scraper.getLobbyistData(220)
        self.assertDictEqual(data, self.lobbyist_220_data)

    def testGetAllLobbyistsData(self):
        scraper = LobbyistsScraper()
        scraper.sources = {
            'index': FileSource(os.path.join(self.DATA_DIR, 'lobbyists_index_only220.html')),
            'lobbyist': FileSource(os.path.join(self.DATA_DIR, 'View_lobbyist_<<id>>.xml')),
            'lobbyist_represent':  FileSource(os.path.join(self.DATA_DIR, 'lobbist_type_<<id>>.xml')),
        }
        scraper.storeAllLobbyistsData()
        self.assertDictEqual(scraper.storages['lobbyist'].data, {220: self.lobbyist_220_data})