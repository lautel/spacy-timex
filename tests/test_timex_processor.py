import pytest
from app.processors.timex_processor import TimexHttpRequestProcessor, TimexHttpResponseProcessor
from unittest.mock import patch, Mock


@pytest.fixture
def req_doc():
    req = {
        "text": "Let's have a meeting on Friday at 11:30"
    }
    return req


@pytest.fixture
def request_processor(req_doc):
    req = Mock()
    req.context = {
        "doc": req_doc
    }
    processor = TimexHttpRequestProcessor(req)
    return processor


@patch.object(TimexHttpRequestProcessor, "process")
class TestClassTimexHttpResponseGenerator(object):

    def test_response_exceptions(self, mock_process, request_processor):
        response_processor = TimexHttpResponseProcessor(request_processor)

        with mock_process:
            mock_process.side_effect = Exception()
            response = response_processor.generate()
            assert type(response) is dict
            assert response["status_info"] == "Failed to process text"
