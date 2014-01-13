# encoding: utf-8

import importlib
import logging

def run(args):
    logging.basicConfig(level=logging.DEBUG)
    if len(args) >= 2:
        module = importlib.import_module(args[0])
        scraperClass = getattr(module, args[1])
        scraper = scraperClass()
        scraper.scrape(*args[2:])
    else:
        raise Exception('invalid args')
