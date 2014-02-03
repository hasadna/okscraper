# encoding: utf-8

class Base(object):
    """
    Base class for source fields
    All source fields should define a get_value method - see Simple for an example
    """
    pass

class Simple(object):
    """
    Simple source field that returns the field_name's value from the data
    """

    def __init__(self, field_name):
        self._field_name = field_name

    def get_value(self, source_data):
        return source_data[self._field_name]

class StringFormat(Base):
    """
    Allow to return string formatted field values from the data
    """

    def __init__(self, string_format, field_names):
        self._string_format = string_format
        self._field_names = field_names

    def get_value(self, source_data):
        return self._string_format % tuple(self._field_names)

class Related(Base):
    """
    return an object generated from a fields processor
    """

    def __init__(self, fields_processor):
        self._fields_processor = fields_processor

    def get_value(self, source_data):
        return self._fields_processor.process(source_data)
