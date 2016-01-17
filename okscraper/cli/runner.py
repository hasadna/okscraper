# encoding: utf-8

import importlib
import logging
import traceback

class Runner(object):
    """
    Provides functionality for running a scraper from the command line
    
    it gets a module_name and looks for a scrapers module under that module name
    
    e.g. if module_name = lobbyists then the scrapers module is under lobbyists.scrapers
    
    it then looks for a MainScraper class in that module and scrapes that class
    
    alternatively - if scraper_class_name is provided it uses that scraper class
    
    also - you can pass arbitrary args and kwargs which are passed to the scraper
    """

    def __init__(self, module_name, scraper_class_name = None, *args, **kwargs):
        if scraper_class_name is None:
            scraper_class_name = 'MainScraper'
        self._module_name = module_name
        self._scraper_class_name = scraper_class_name
        if 'extra_scraper_args' in kwargs:
            args += tuple(kwargs['extra_scraper_args'])
            del kwargs['extra_scraper_args']
        self._args = args
        self._kwargs = kwargs
        self.post_init()

    def post_init(self):
        pass

    def post_run(self):
        pass

    def run(self):
        try:
            module = importlib.import_module('%s.scrapers' % self._module_name)
            scraperClass = getattr(module, self._scraper_class_name)
            scraper = scraperClass()
            if len(self._kwargs) > 0 and len(self._args) > 0:
                result = scraper.scrape(*self._args, **self._kwargs)
            elif len(self._args) > 0:
                result = scraper.scrape(*self._args)
            elif len(self._kwargs) > 0:
                result = scraper.scrape(**self._kwargs)
            else:
                result = scraper.scrape()
        finally:
            self.post_run()
        return result


class LogRunner(Runner):
    """Adds logging capabilities to the Runner class"""

    def _getLogLevelFromVerbosity(self, verbosity):
        verbosities = {
            '1': logging.WARN,
            '2': logging.INFO,
            '3': logging.DEBUG
        }
        return verbosities.get(str(verbosity), logging.ERROR)

    def __init__(self, *args, **kwargs):
        if 'log_handler' in kwargs:
            logger = logging.getLogger()
            logger.setLevel(logging.DEBUG)
            handler = kwargs.pop('log_handler')
            if 'log_verbosity' in kwargs:
                level = self._getLogLevelFromVerbosity(kwargs.pop('log_verbosity'))
                handler.setLevel(level)
            logger.addHandler(handler)
        super(LogRunner, self).__init__(*args, **kwargs)

    def run(self):
        try:
            return super(LogRunner, self).run()
        except:
            exc = traceback.format_exc()
            logging.getLogger(self.__class__.__module__+'('+self.__class__.__name__+')').exception(exc)
            return None


class _DbLogHandler(logging.Handler):

    def __init__(self, *args, **kwargs):
        self.log_runner = kwargs.pop('log_runner')
        super(_DbLogHandler, self).__init__(*args, **kwargs)

    def emit(self, record):
        self.log_runner.on_dblog_emit(record)


class DbLogRunner(LogRunner):
    """Adds capabilities relevant to db logging to the LogRunner class"""

    def __init__(self, *args, **kwargs):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        handler = _DbLogHandler(log_runner=self)
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)
        super(DbLogRunner, self).__init__(*args, **kwargs)

    def on_dblog_emit(self, record):
        raise Exception('on_dblog_emit must be implemented by extending classes')