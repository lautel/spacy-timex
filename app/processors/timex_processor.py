from app.facade import TimexFacade
from app.processors.abstract_processor import AbstractHttpProcessor, AbstractHttpProcessorResponse


class TimexHttpRequestProcessor(AbstractHttpProcessor):
    SERVICE_LABEL = "App:TimexRequest"

    __slots__ = "_doc", "facade"

    def __init__(self, request):
        AbstractHttpProcessor.__init__(self)

        self._doc = request.context["doc"]
        self.facade = TimexFacade()

    def process(self) -> dict:
        response = dict()

        # TODO. Complete
        text_processed = self.facade.process("")
        response["text"] = text_processed
        
        return response

    @property
    def doc(self):
        return self._doc


class TimexHttpResponseProcessor(AbstractHttpProcessorResponse):
    SERVICE_LABEL = "App:TimexResponse"

    def __init__(self, processor):
        super().__init__()
        self._processor = processor
        self._id = processor.id

    def generate(self) -> dict:
        response = self.get_initialization()

        try:
            result = self._processor.process()
        except Exception:
            response["status"] = "NO OK"
            response["status_info"] = f"Failed to process text"
            return response

        response["text"] = result["text"]

        # TODO. Complete code

        return response
