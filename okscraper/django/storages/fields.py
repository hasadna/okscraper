# encoding: utf-8

import source_fields
import model_fields


def get_model_field(model_field):
    """
    if the model_field is an instance of model_field.Base - return that field
    otherwise instansiate a model_field.Simple object with field_name = model_field
    """
    if isinstance(model_field, model_fields.Base):
        return model_field
    else:
        return model_fields.Simple(field_name = model_field)


def get_source_field(source_field):
    """
    if the source_field is an instance of source_field.Base - return that field
    otherwise instansiate a source_field.Simple object with field_name = source_field
    """
    if isinstance(source_field, source_fields.Base):
        return source_field
    else:
        return source_fields.Simple(field_name = source_field)


def get_field(field):
    """
    if the field is an instance of Base - return that field
    otherwise instanstiate a Simple field with model_field and source_field equals to field
    """
    if isinstance(field, Base):
        return field
    else:
        return Simple(model_field = field, source_field = field)


class FieldsProcessor(object):
    """
    the fields processor gets a model class and a list of fields
    then when process is called it uses the source_data to create an object
    finally process method returns a saved object
    """

    def __init__(self, model, fields):
        self._model = model
        self._fields = []
        for field in fields:
            self._fields.append(get_field(field))

    def _call_fields(self, method, break_on_return = False, *args, **kwargs):
        for field in self._fields:
            if hasattr(field, method):
                ret = getattr(field, method)(*args, **kwargs)
                if break_on_return:
                    return ret
        return None

    def _create_obj(self):
        return self._model()

    def process(self, source_data):
        obj = self._call_fields('create_obj', break_on_return = True, model = self._model, source_data = source_data)
        if obj is None:
            obj = self._create_obj()
        self._call_fields('process', source_data = source_data, obj = obj)
        obj.save()
        self._call_fields('post_save', source_data = source_data, obj = obj)
        return obj


class Base(object):
    """
    Base class for all fields
    all fields must extend this class because it is used for identifying source fields
    fields can define method create_obj / process / post_save - see in FieldsProcessor
    """
    pass


class Simple(Base):
    """
    Simple field that gets a value from the source_field and store it in the model_field
    """

    def __init__(self, model_field, source_field):
        self._model_field = get_model_field(model_field)
        self._source_field = get_source_field(source_field)

    def _get_value(self, source_data):
        return self._source_field.get_value(source_data)

    def process(self, source_data, obj):
        self._model_field.set_value(obj, self._get_value(source_data))


class Primary(Simple):
    """
    Same as Simple field except it tries to get an existing object based on this field
    if such an object exists - the process will update that object instead of creating a new one
    There can be only one! (Primary field)
    """

    def create_obj(self, model, source_data):
        qs = model.objects.filter(**{
            self._model_field.get_field_name(): self._source_field.get_value(source_data)
        })
        return qs[0] if qs.count() > 0 else None


class ManyToMany(Base):
    """
    special field that doesn't store anything in the object
    instead - it runs after the object was saved
    then it stores that object in another object's related field
    """

    def __init__(self, source_field, related_field_name):
        self._source_field = get_source_field(source_field)
        self._related_field_name = related_field_name

    def post_save(self, source_data, obj):
        other_obj = self._source_field.get_value(source_data)
        getattr(other_obj, self._related_field_name).add(obj)
        other_obj.save()