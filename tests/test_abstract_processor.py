from abc import ABCMeta
from dataclasses import dataclass

from app.processors.abstract_processor import AbstractHttpProcessor, AbstractHttpProcessorResponse


def test_processor():
    AbstractHttpProcessor.__abstractmethods__ = set()

    @dataclass
    class Dummy(AbstractHttpProcessor):
        abs: AbstractHttpProcessor
        _id = 1234

    test_abc = AbstractHttpProcessor()
    d = Dummy(test_abc)
    d.process()

    assert isinstance(AbstractHttpProcessor, ABCMeta)
    assert d.id == 1234


def test_processor_response():
    AbstractHttpProcessorResponse.__abstractmethods__ = set()

    @dataclass
    class Dummy(AbstractHttpProcessorResponse):
        abs: AbstractHttpProcessorResponse
        _id = 5678

    test_abc = AbstractHttpProcessorResponse()
    d = Dummy(test_abc)
    d.generate()
    response = d.get_initialization()

    assert isinstance(AbstractHttpProcessorResponse, ABCMeta)
    assert d.id == 5678
    assert isinstance(response, dict)
    assert response["status"] == "OK"
    assert response["status_info"] == "App_info: Request successfully processed"
