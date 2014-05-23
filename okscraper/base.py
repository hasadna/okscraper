from unittest import TestCase
import os
import inspect
import logging

class BaseScraper(object):
    """
        Abstract Scraper class - should be extended by concrete scraper objects

        You must declare the following::

            def __init__(self, *args, **kwargs):
                self.source = (an object derived from a class based on okscraper.sources.BaseSource)
                self.storage = (an object derived from a class based on okscraper.storages.BaseStorage)

            def _scrape(self):
                # here you do the actual scraping based on source and storing to storage
    """
    def __init__(self, *args, **kwargs):
        pass

    def _scrape(self, *args, **kwargs):
        raise Exception('_scrape method must be implemented by extending classes')

    def _getLogger(self):
        return logging.getLogger(self.__class__.__module__+'('+self.__class__.__name__+')')

    def scrape(self, *args, **kwargs):
        self._scrape(*args, **kwargs)
        self.storage.commit()
        return self.storage.get()

class ParsingFromFileTestCase(TestCase):
    """
        base class for testing scrapers with input from a file
        
        minimal implementation sample::

            class MyScraperTestCase(ParsingFromFileTestCase):
                def _getScraperClass(self):
                    return MyScraper

                def _getFilename(self):
                    # this is a file containing test data
                    return 'my_data_<<id>>.xml'

                def testParsing(self):
                    self.assertScrape(
                        args=(220),
                        expectedData={'id': 220, 'name':'Hello World',}
                    )
    """

    def _getScraperClass(self):
        raise Exception('you must implement the _GetScraperClass or _getScraper methods')

    def _getScraper(self):
        scraperClass = self._getScraperClass()
        return scraperClass()

    def _getFilename(self):
        return self._filename

    def _getDataDir(self):
        _file_ = inspect.getfile(self.__class__)
        return os.path.join(os.path.abspath(os.path.dirname(_file_)), 'testdata')

    def _getSource(self):
        from okscraper.sources import FileSource
        return FileSource(os.path.join(self._getDataDir(), self._getFilename()))

    def _getStorageClass(self):
        return self.scraper.storage.getBaseStorage()

    def _getStorage(self):
        storageClass = self._getStorageClass()
        return storageClass()

    def _assertParseSuccessful(self, expected_data):
        self.scraper.storage.assertEquals(self, expected_data)

    def _initScraper(self):
        self.scraper = self._getScraper()
        self.scraper.source = self._getSource()
        self.scraper.storage = self._getStorage()

    def _init(self):
        self._filename = None
        self.scraper = None

    def assertScrape(self, expectedData, args=(), kwargs={}, filename=None):
        self._init()
        if filename is not None: self._filename = filename
        self._initScraper()
        self.scraper.scrape(*args, **kwargs)
        self._assertParseSuccessful(expectedData)