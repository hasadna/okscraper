
class BaseStorage(object):
    """Abstract class
        implementing classes must define the following methods:
        store - store data
        commit - (optional, commit the data)
        get - (optioanl, return stored data or pointer to stored data)
    """
    def store(self):
        raise Exception('store must be implemented by extending classes')

    def commit(self):
        pass

    def get(self):
        return None

class DataBasedStorage(BaseStorage):

    def __init__(self):
        self._commitInterval = 20
        self._storeCounter = 0
        self._data = self._getEmptyData()
        self._tmpData = self._getEmptyData()

    def _getEmptyData(self):
        raise Exception('_getEmptyData needs to be implemented by extending classes')

    def _addValueToData(self, data):
        raise Exception('_addValueToData needs to be implemented by extending classes')

    def _addDataToData(self, targetData, sourceData):
        raise Exception('_addDataToData needs to be implemented by extending classes')

    def store(self, *args, **kwargs):
        self._addValueToData(self._tmpData, *args, **kwargs)
        self._storeCounter = self._storeCounter + 1
        if self._storeCounter > self._commitInterval:
            self.commit()

    def commit(self):
        self._addDataToData(self._data, self._tmpData)
        self._storeCounter = 0
        self._tmpData = self._getEmptyData()

    def get(self):
        self.commit()
        return self._data

class DictStorage(DataBasedStorage):

    def _getEmptyData(self):
        return {}

    def _addValueToData(self, data, key, value):
        data[key] = value

    def _addDataToData(self, targetData, sourceData):
        targetData.update(sourceData)

    def getBaseStorage(self):
        return DictStorage

    def assertEquals(self, testCase, expected_data):
        testCase.assertDictEqual(self._data, expected_data)

    def storeDict(self, data):
        for key in data:
            self.store(key, data[key])

class ListStorage(DataBasedStorage):

    def _getEmptyData(self):
        return []

    def _addValueToData(self, data, value):
        data.append(value)

    def _addDataToData(self, targetData, sourceData):
        for item in sourceData:
            targetData.append(item)

    def getBaseStorage(self):
        return ListStorage

    def assertEquals(self, testCase, expected_data):
        testCase.assertListEqual(self._data, expected_data)