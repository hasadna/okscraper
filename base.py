from unittest import TestCase

class Scraper:

    storages = {}
    sources = {}

    def _fetch(self, sourceId, *args, **kwargs):
        return self.sources[sourceId].fetch(*args, **kwargs)

    def _store(self, storageId, *args, **kwargs):
        self.storages[storageId].store(*args, **kwargs)

class ScraperTestCase(TestCase):

    pass