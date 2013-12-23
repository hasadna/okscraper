import re

class BaseSource():
    """Abstract BaseSource
        extending classes must implement a fetch method which returns the data
    """

class BaseStringParamsSource():

    def __init__(self, source_string):
        self._source_string = source_string

    def fetch(self, *args, **kwargs):
        args = list(args)
        src = self._source_string
        identifiers = re.findall(r"<<(\w*)>>", src)
        while len(args) > 0 and len(identifiers) > 0:
            identifier = identifiers.pop(0)
            arg = args.pop(0)
            src = src.replace('<<{}>>'.format(identifier), str(arg))
        return self._fetch(src)

class UrlSource(BaseStringParamsSource):
    pass

class FileSource(BaseStringParamsSource):

    def _fetch(self, filepath):
        with file(filepath) as f:
            return f.read()
