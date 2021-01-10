import falcon
import json
from app.api_falcon import HealthCheckService, TimexService, api_falcon_init
from app.facade import TimexFacade
from unittest.mock import Mock


class TestClassHealthCheckService(object):
    def test_on_get(self):
        resp = falcon.Response()

        HealthCheckService.on_get(None, resp)

        response_dict = {"status": "OK", "status_info": "Service working nicely"}

        assert resp.status == falcon.HTTP_200
        assert resp.body == json.dumps(response_dict)


class TestClassTimexService(object):
    def test_on_post(self):
        request_doc = {
           "text": "Let's have a meeting on Friday at 11:30"
        }

        resp = falcon.Response()

        req = Mock()
        req.context = {
            "doc": request_doc
        }

        TimexService().on_post(req, resp)

        assert resp.status == falcon.HTTP_200


def test_falcon_api_init():
    app = api_falcon_init()

    assert isinstance(app, falcon.API)
