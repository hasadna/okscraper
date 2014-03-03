# encoding: utf-8

import unittest
from mock_module.scrapers import DummyStorage, DummySource, DummyScraper
import logging
from okscraper.base import ParsingFromFileTestCase

class TestBase(unittest.TestCase):

    def test_scraper(self):
        class Scraper(DummyScraper):
            def _scrape(self, val):
                self.storage.store(val)
        scraper = Scraper()
        self.assertEqual(scraper.scrape('test'), 'test')

    def test_scraper_logger(self):
        class Scraper(DummyScraper):
            def _scrape(self, val):
                self.storage.store(self._getLogger())
        scraper = Scraper()
        logger = scraper.scrape(None)
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, 'testBase(Scraper)')


class TestParsingFromFileTestCase_Minimal(ParsingFromFileTestCase):

    def _getScraperClass(self):
        return DummyScraper

    def _getFilename(self):
        return 'TestParsingFromFileTestCase_Minimal.txt'

    def testParsing(self):
        self.assertScrape(expectedData='testing 123')

class TestParsingFromFileTestCase_Minimal(ParsingFromFileTestCase):

    def _getScraperClass(self):
        return DummyScraper

    def _getFilename(self):
        return 'TestParsingFromFileTestCase_Minimal.txt'

    def testParsing(self):
        self.assertScrape(expectedData='testing 123')
