
class BaseStorage():
    """Abstract class
        implementing classes must define the following methods:
        store - store data
        commit - (optional, commit the data)
    """
    def commit(self):
        pass


class DictStorage(BaseStorage):

    _data = {}

    def store(self, key, value):
        self._data[key] = value

    def getBaseStorage(self):
        return DictStorage

    def assertEquals(self, testCase, expected_data):
        testCase.assertDictEqual(self._data, expected_data)

class ListStorage(BaseStorage):

    _data = []

    def store(self, value):
        self._data.append(value)

    def getBaseStorage(self):
        return ListStorage

    def assertEquals(self, testCase, expected_data):
        testCase.assertListEqual(self._data, expected_data)