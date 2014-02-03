# encoding: utf-8

import importlib

class Runner(object):
    """
    Provide functionality for running a scraper from the command line
    it gets a module_name and looks for a scrapers module under that module name
    e.g. if module_name = lobbyists then the scrapers module is under lobbyists.scrapers
    it them looks for a MainScraper class in that module and scrapes that class
    alternatively - if scraper_class_name is provided it uses that scraper class
    also - you can pass arbitrary args and kwargs which are passed to the scraper
    """

    def __init__(self, module_name, scraper_class_name = None, *args, **kwargs):
        if scraper_class_name is None:
            scraper_class_name = 'MainScraper'
        self._module_name = module_name
        self._scraper_class_name = scraper_class_name
        self._args = args
        self._kwargs = kwargs

    def run(self):
        module = importlib.import_module('%s.scrapers' % self._module_name)
        scraperClass = getattr(module, self._scraper_class_name)
        scraper = scraperClass()
        scraper.scrape(*self._args, **self._kwargs)