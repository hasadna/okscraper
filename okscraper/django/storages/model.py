# encoding: utf-8


from okscraper.storages import DictStorage, ListStorage


class ModelDictStorage(DictStorage):
    """
    Storage provider that stores a dict into a django model
    it accepts a fields_processor object which defines how the data will be processed
    see okscraper.storages.fields.FieldsProcessor for details
    """

    _commitInterval = -1

    def __init__(self, fields_processor):
        super(ModelDictStorage, self).__init__()
        self._fields_processor = fields_processor

    def commit(self):
        super(ModelDictStorage, self).commit()
        data = self.get()
        self._data = self._fields_processor.process(data)


class ModelListDictStorage(ListStorage):
    """
    storage for a list of dicts
    each dict is processed using a FieldsProcessor
    see okscraper.storages.fields.FieldsProcessor for details
    """

    _commitInterval = 0

    def __init__(self, fields_processor):
        super(ModelListDictStorage, self).__init__()
        self._fields_processor = fields_processor

    def commit(self):
        newTmpData = []
        for data in self._tmpData:
            newTmpData.append(self._fields_processor.process(data))
        self._tmpData = newTmpData
        super(ModelListDictStorage, self).commit()
