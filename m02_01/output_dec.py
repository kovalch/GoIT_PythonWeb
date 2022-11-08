from abc import ABC, abstractmethod


class AbstractOutput(ABC):
    """ Abstract base class for output in the terminal"""

    def __init__(self, data):
        self.data = data

    @abstractmethod
    def output(self):
        pass


class CLIOutput(AbstractOutput):
    """ Class for output """

    def output(self):
        return self.data


def async_output(func):
    """ Decorator for static functions """
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        data.__str__()
        if data:
            result = CLIOutput(data)
            result.output()
            return result

        return wrapper
