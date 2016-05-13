import re, requests

class BaseSource(object):
    """
        Abstract BaseSource
        
        extending classes must implement a fetch method which returns the input data
    """

class BaseStringParamsSource(BaseSource):

    def __init__(self, source_string):
        self._source_string = source_string

    def get_source_string(self, *args, **kwargs):
        args = list(args)
        src = self._source_string
        identifiers = re.findall(r"<<(\w*)>>", src)
        while len(args) > 0 and len(identifiers) > 0:
            identifier = identifiers.pop(0)
            arg = args.pop(0)
            src = src.replace('<<{}>>'.format(identifier), str(arg))
        return src

    def _fetch(self, *args, **kwargs):
        raise NotImplementedError()

    def fetch(self, *args, **kwargs):
        return self._fetch(self.get_source_string(*args, **kwargs))

class UrlSource(BaseStringParamsSource):
    """fetch data from a url"""
    def _fetch(self, url):
        return requests.get(url).text

class FileSource(BaseStringParamsSource):
    """fetch data from a file"""
    def _fetch(self, filepath):
        with open(filepath) as f:
            return f.read()

class ScraperSource(BaseSource):
    """fetch data from an okscraper"""

    def __init__(self, scraper):
        self._scraper = scraper

    def fetch(self, *args, **kwargs):
        return self._scraper.scrape(*args, **kwargs)
