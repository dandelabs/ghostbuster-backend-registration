from .singleton import Singleton

class ResponseHttp(metaclass=Singleton):

    def __init__(self, _data, _errors):

        if _errors is None:
            _errors = ''

        if _data is None:
            _data = ''

        self.data = {
            'results': _data,
            'errors': _errors
        }
