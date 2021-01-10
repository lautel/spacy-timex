from abc import ABC, ABCMeta, abstractmethod


class AbstractHttpProcessor(ABC):
    __metaclass__ = ABCMeta

    def __init__(self):
        super().__init__()
        self._id = 0

    @abstractmethod
    def process(self):
        pass

    @property
    def id(self):
        return self._id


class AbstractHttpProcessorResponse(ABC):

    def __init__(self):
        super().__init__()
        self._id = 0

    @abstractmethod
    def generate(self):
        pass

    @staticmethod
    def get_initialization() -> dict:
        response = dict()

        response["status"] = "OK"
        response["status_info"] = "App_info: Request successfully processed"

        return response

    @property
    def id(self):
        return self._id
