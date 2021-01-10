import json
import falcon
import logging as log
import configuration.environment_config as env_config

from wsgiref import simple_server
from app.processors.timex_processor import TimexHttpRequestProcessor
from app.processors.timex_processor import TimexHttpResponseProcessor
from app.facade import TimexFacade
from utils.load_config import load_service_config


class RequestChecker(object):
    """ Falcon’s middleware interface """

    def process_request(self, req: falcon.Request, resp: falcon.Response) -> None:
        """
        Process the request before routing it. Only applies to POST requests.
        :param req: Request object that will eventually be routed to an on_* responder method.
        :param resp: Response object that will be routed to the on_* responder.
        :return: None
        """

        if req.method == "POST":
            if "application/json" not in req.content_type:
                log.error("File Open Error - Content type parameter in the request is invalid.", access="end")
                raise falcon.HTTPUnsupportedMediaType(
                    "Unsupported Media Type - The service only allows application/json documents")

            if req.content_length in (None, 0):
                log.error("File Open Error - empty request", access="end")
                raise falcon.HTTPBadRequest("Empty request", "A valid JSON document is required.")

            body = req.stream.read()

            if not body:
                log.error("File Open Error - empty Body", access="end")
                raise falcon.HTTPBadRequest("Empty request body", "A valid JSON document is required.")

            try:
                req.context["doc"] = json.loads(body.decode("utf-8"))
            except (ValueError, UnicodeDecodeError):
                raise falcon.HTTPError(falcon.HTTP_753,
                                       "Malformed JSON",
                                       "The request body could not be decoded. "
                                       "The JSON was incorrect or not encoded as UTF-8.")


class TimexService:
    @staticmethod
    def on_post(req, resp):

        # Process Request
        processor = TimexHttpRequestProcessor(req)
        log.info("/timex service got requested", access="start")
        response_generator = TimexHttpResponseProcessor(processor)
        response_dict = response_generator.generate()

        if not response_dict:
            resp.status = falcon.HTTP_500
        else:
            if response_dict["status"] == "OK":
                log.info("Query was successfully processed", access="end")

            # Response
            resp.status = falcon.HTTP_200
            resp.append_header("Id", response_generator.id)
            resp.body = json.dumps(response_dict)


class HealthCheckService:
    @staticmethod
    def on_get(req, resp):
        response_dict = dict()
        response_dict["status"] = "OK"
        response_dict["status_info"] = "Service working nicely"
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(response_dict)


# These are all the services available, which are enabled in configuration
EXPOSED_SERVICE_CLASSES = {"health": HealthCheckService,
                           "timex": TimexService}


def api_falcon_init():
    app = falcon.API(middleware=[RequestChecker(), ])

    active_services = load_service_config()

    # Initialize Singletons
    log.info("*** Starting services ***")
    timex = TimexFacade()

    # Load active services
    for service_name in active_services:
        try:
            service = EXPOSED_SERVICE_CLASSES[service_name]()
            app.add_route(f"/{service_name}", service)
            log.info(f"Service {service_name} started")
        except Exception as e:
            log.warning(f"Service {service_name} not found, exception: {e}")

    log.info("All Services Started")
    return app


if __name__ == "__main__":
    app = api_falcon_init()

    http = simple_server.make_server(env_config.API_HOST, env_config.API_PORT, app)
    http.serve_forever()


app = api_falcon_init()
