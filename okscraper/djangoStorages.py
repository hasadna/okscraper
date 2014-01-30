# encoding: utf-8

from okscraper.storages import DictStorage, ListStorage

class ModelDictStorage(DictStorage):

    _commitInterval = -1

    def __init__(self, model, model_fields_map = None):
        super(ModelDictStorage, self).__init__()
        self.model_fields_map = {} if model_fields_map is None else model_fields_map
        self.model = model

    def commit(self):
        super(ModelDictStorage, self).commit()
        data = self.get()
        processed_data_keys = []
        kwargs = {}
        for model_field_name in self.model_fields_map:
            model_field_data_key = self.model_fields_map[model_field_name]
            if model_field_data_key is not None:
                if isinstance(model_field_data_key, BaseModelValue):
                    (model_field_value, data_keys) = model_field_data_key.process(data)
                    processed_data_keys += data_keys
                else:
                    model_field_value = data[model_field_data_key]
                if not isinstance(model_field_value, ModelValueNone):
                    kwargs[model_field_name] = model_field_value
        for key in data:
            if key not in processed_data_keys and key is not None:
                kwargs[key] = data[key]
        self._data = self.model.objects.create(**kwargs)

class ModelListDictStorage(ListStorage):

    _commitInterval = 0

    def __init__(self, *args, **kwargs):
        super(ModelListDictStorage, self).__init__()
        self._args = args
        self._kwargs = kwargs

    def commit(self):
        newTmpData = []
        for data in self._tmpData:
            dictStorage = ModelDictStorage(*self._args, **self._kwargs)
            dictStorage.storeDict(data)
            dictStorage.commit()
            newTmpData.append(dictStorage.get())
        self._tmpData = newTmpData
        super(ModelListDictStorage, self).commit()

class BaseModelValue(object):

    def process(self, data):
        raise Exception('process method must be implemented by extending classes')

class ModelValueRelated(BaseModelValue):

    def __init__(self, model, fieldsMap):
        self._model = model
        self._fieldsMap = fieldsMap

    def process(self, data):
        processed_data_keys = []
        kwargs = {}
        for model_field_name in self._fieldsMap:
            data_field_name = self._fieldsMap[model_field_name]
            if isinstance(data_field_name, BaseModelValue):
                (value, data_keys) = data_field_name.process(data)
                processed_data_keys += data_keys
            else:
                value = data[data_field_name]
                processed_data_keys.append(data_field_name)
            kwargs[model_field_name] = value
        value = self._model.objects.create(**kwargs)
        return (value, processed_data_keys)

class ModelValueStringConcat(BaseModelValue):

    def __init__(self, *args):
        self._args = args

    def process(self, data):
        data_keys = []
        vals = []
        for arg in self._args:
            vals.append(data[arg])
            data_keys.append(arg)
        value = ' '.join(vals)
        return (value, data_keys)

class ModelValueNone(BaseModelValue):

    def __init__(self, *args):
        self._args = args

    def process(self, data):
        return (ModelValueNone(), self._args)