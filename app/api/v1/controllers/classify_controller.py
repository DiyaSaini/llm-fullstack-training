"""
Classify controller.

ASSOCIATE 2 — implement the handle() method below.
"""

from app.api.v1.schemas.requests.classify import ClassifyRequest
from app.api.v1.schemas.responses.classify import ClassifyResponse
from app.core.pipeline.classify_pipeline import ClassifyPipeline
from app.logging import get_logger

logger = get_logger(__name__)


class ClassifyController:
    """Handles HTTP concerns for the /classify endpoint."""

    def __init__(self, pipeline: ClassifyPipeline) -> None:
        self.pipeline = pipeline

    def handle(self, request: ClassifyRequest) -> ClassifyResponse:
        """
        Process a classify request.

        TODO:
            - Call self.pipeline.execute(request)
            - Catch ValueError → raise HTTPException 422 with the error message
            - Catch LLMProviderError → raise HTTPException 502 with a safe message
            - Catch any other Exception → log it, raise HTTPException 500
            - Return the result on success
        """
        raise NotImplementedError
