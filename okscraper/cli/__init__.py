# encoding: utf-8

import importlib
import logging

def run(args):
    if len(args) > 0:
        module = importlib.import_module(args[0])
        runScraperClassName = None
        scraperArgs = args[1:]
        if 'okscrapers' in dir(module):
            scraperClasses = module.okscrapers
            scraperClassNames = [scraperClass.__name__ for scraperClass in scraperClasses]
            if len(args) > 1:
                if args[1] in scraperClassNames:
                    runScraperClassName = args[1]
                    scraperArgs = args[2:]
        elif len(args) > 1:
            runScraperClassName = args[1]
            scraperArgs = args[2:]
        else:
            raise InvalidArgsException('invalid args')
        if runScraperClassName is None:
            if 'default_okscrapers' in dir(module):
                runScraperClasses = module.default_okscrapers
            else:
                runScraperClasses = module.okscrapers
        else:
            scraperClass = getattr(module, args[1])
            runScraperClasses = [scraperClass]
        for scraperClass in runScraperClasses:
            logging.getLogger('okscraper.cli').info('running scraper class %s with args %s' % (scraperClass.__name__, scraperArgs,))
            scraper = scraperClass()
            scraper.scrape(*scraperArgs)
    else:
        raise InvalidArgsException('invalid args')

class InvalidArgsException(Exception):
    pass
