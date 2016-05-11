# encoding: utf-8

from okscraper.base import BaseScraper
from okscraper.storages import BaseStorage
from okscraper.sources import BaseSource

class DummyStorage(BaseStorage):

    def __init__(self):
        self._val = None
        self._tmpval = None

    def store(self, val):
        self._tmpval = val

    def commit(self):
        self._val = self._tmpval

    def get(self):
        return self._val

    def getBaseStorage(self):
        return DummyStorage

    def assertEquals(self, testCase, expected_data):
        testCase.assertEqual(self._val, expected_data)

class DummySource(BaseSource):

    def __init__(self, data = ''):
        self._data = data

    def fetch(self):
        return self._data

class DummyScraper(BaseScraper):

    def __init__(self):
        self.source = DummySource()
        self.storage = DummyStorage()

    def _scrape(self):
        self.storage.store(self.source.fetch())


class MainScraper(DummyScraper):

    def _getTitle(self):
        return 'MainScraper'

    def _scrape(self, extra_data_1='', extra_data_2=''):
        self.storage.store('ok_%s%s%s%s'%(self._getTitle(),extra_data_1, extra_data_2, self.source.fetch()))


class OtherScraper(MainScraper):

    def _getTitle(self):
        return 'OtherScraper'


class LoggingScraper(MainScraper):

    def _getTitle(self):
        self._getLogger().info('_getTitle')
        return 'LoggingScraper'

    def _scrape(self, *args, **kwargs):
        if 'test_logs' in kwargs:
            for log in kwargs.pop('test_logs'):
                self._getLogger().log(log['level'], log['msg'])
        if 'fake_error' in kwargs:
            xxx()
        super(LoggingScraper, self)._scrape(*args, **kwargs)