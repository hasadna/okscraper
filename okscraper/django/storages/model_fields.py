# encoding: utf-8

class Base(object):
    """
    Base class for model_Fields
    all model fields should define a set_value method (see Simple for an example)
    for some usages you might also need get_field_name but it's not required
    """
    pass

class Simple(Base):
    """
    Simple model field - store the value in the object's field name
    """

    def __init__(self, field_name):
        self._field_name = field_name

    def get_field_name(self):
        return self._field_name

    def set_value(self, obj, value):
        setattr(obj, self._field_name, value)