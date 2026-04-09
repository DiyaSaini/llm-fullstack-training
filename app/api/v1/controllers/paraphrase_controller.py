"""
Paraphrase controller.

ASSOCIATE 6 — implement the handle() method below.

The controller is responsible for:
    - Receiving the validated request from the router
    - Calling the pipeline
    - Translating exceptions into appropriate HTTP responses
    - Returning the response object

It does NOT contain business logic. That lives in the service.
"""

from app.api.v1.schemas.requests.paraphrase import ParaphraseRequest
from app.api.v1.schemas.responses.paraphrase import ParaphraseResponse
from app.core.pipeline.paraphrase_pipeline import ParaphrasePipeline
from app.logging import get_logger

logger = get_logger(__name__)


class ParaphraseController:
    """Handles HTTP concerns for the /paraphrase endpoint."""

    def __init__(self, pipeline: ParaphrasePipeline) -> None:
        self.pipeline = pipeline

    def handle(self, request: ParaphraseRequest) -> ParaphraseResponse:
        """
        Process a paraphrase request.

        TODO:
            - Call self.pipeline.execute(request)
            - Catch ValueError → raise HTTPException 422 with the error message
            - Catch LLMProviderError → raise HTTPException 502 with a safe message
            - Catch any other Exception → log it, raise HTTPException 500
            - Return the result on success

        Args:
            request: Validated ParaphraseRequest from the router.

        Returns:
            ParaphraseResponse.

        Raises:
            HTTPException 422: If input validation fails inside the service.
            HTTPException 502: If the LLM provider call fails.
            HTTPException 500: For any unexpected error.
        """
        raise NotImplementedError
