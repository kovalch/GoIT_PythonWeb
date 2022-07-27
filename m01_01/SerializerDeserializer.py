from abc import ABCMeta, abstractmethod, ABC
import logging
log = logging.getLogger(__name__)
import os
import json
import pickle
from pprint import pprint
import yaml

"""
Serialization of containers with Python data into json, bin and yaml files
"""
class ISerDe(metaclass=ABCMeta):
    """Serialization/Deserialization Interface"""

    def __init__(self, data, file_name):
        self.data = data
        self._file_name = None
        self.file_name = file_name

    @property
    @abstractmethod
    def file_name(self):
        ...

    @file_name.setter
    @abstractmethod
    def file_name(self, file_name):
        ...

    @abstractmethod
    def serialize(self):
        pass

    @abstractmethod
    def deserialize(self):
        pass


class JsonSerDe(ISerDe):

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, file_name):
        """ Validate a submission file name """

        extension = ".json"
        if file_name is None:
            raise LookupError('The file name argument is mandatory')

        if os.path.splitext(file_name)[-1] == extension:
            self._file_name = file_name
        else:
            self._file_name = os.path.splitext(file_name)[0] + extension
            log.warning(f'File name with not correct extension is used, changing to {self._file_name}')

    def serialize(self):
        with open(self.file_name, "w") as file:
            json.dump(self.data, file)

    def deserialize(self):
        with open(self._file_name, "r") as file:
            data = json.load(file)
        pprint(data)


class BinSerDe(ISerDe):

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, file_name):
        """ Validate a submission file name """

        extension = ".bin"
        if file_name is None:
            raise LookupError('The file name argument is mandatory')

        if os.path.splitext(file_name)[-1] == extension:
            self._file_name = file_name
        else:
            self._file_name = os.path.splitext(file_name)[0] + extension
            log.warning(f'File name with not correct extension is used, changing to {self._file_name}')

    def serialize(self):
        with open(self.file_name, "wb") as file:
            pickle.dump(self.data, file)

    def deserialize(self):
        with open(self._file_name, "rb") as file:
            data = pickle.load(file)
        pprint(data)


class YamlSerDe(ISerDe):

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, file_name):
        """ Validate a submission file name """

        extension = ".yaml"
        if file_name is None:
            raise LookupError('The file name argument is mandatory')

        if os.path.splitext(file_name)[-1] == extension:
            self._file_name = file_name
        else:
            self._file_name = os.path.splitext(file_name)[0] + extension
            log.warning(f'File name with not correct extension is used, changing to {self._file_name}')

    def serialize(self):
        with open(self.file_name, "w") as file:
            yaml.dump(self.data, file)

    def deserialize(self):
        with open(self._file_name, "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        pprint(data)



if __name__ == '__main__':

    dataset = {'name': 'Milla', 'surname': 'Smith', 'age': 44,
               'phone_numbers': ['+4174995456', '+4092324354306'],
               'email': "Milla@gmail.com"}

    ser_de = BinSerDe(dataset, 'DB_Milla.bla')
    ser_de.serialize()
    ser_de.deserialize()


