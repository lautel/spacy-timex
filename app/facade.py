import logging as log
from datetime import datetime
from utils.load_config import load_timeout


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class TimexFacade(object, metaclass=Singleton):
    """
    Core class to manage modules calls and structured responses.
    The Facade class provides a simple interface to the complex logic of one or
    several subsystems. The Facade delegates the client requests to the
    appropriate objects within the subsystem. The Facade is also responsible for
    managing their lifecycle. All of this shields the client from the undesired
    complexity of the subsystem.
    """

    __slots__ = "max_time"

    def __init__(self):
        self.max_time = load_timeout()

    def process(self, text: str) -> str:
        text_processed = ""

        st = datetime.now()

        # TODO. Code here

        elapsed_time = datetime.now() - st
        if elapsed_time.seconds > self.max_time:
            log.error(f"Processing timeout ({elapsed_time.seconds}.{elapsed_time.microseconds // 1000:03}"
                      f">{self.max_time} s)")
            raise Exception("Timeout while processing the request.")

        return text_processed
