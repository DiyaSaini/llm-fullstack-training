"""
Qa controller.

ASSOCIATE 5 — implement the handle() method below.

The controller is responsible for:
    - Receiving the validated request from the router
    - Calling the pipeline
    - Translating exceptions into appropriate HTTP responses
    - Returning the response object

It does NOT contain business logic. That lives in the service.
"""

from app.api.v1.schemas.requests.qa import QARequest
from app.api.v1.schemas.responses.qa import QAResponse
from app.core.pipeline.qa_pipeline import QAPipeline
from app.logging import get_logger

logger = get_logger(__name__)


class QaController:
    """Handles HTTP concerns for the /qa endpoint."""

    def __init__(self, pipeline: QAPipeline) -> None:
        self.pipeline = pipeline

    def handle(self, request: QARequest) -> QAResponse:
        """
        Process a qa request.

        TODO:
            - Call self.pipeline.execute(request)
            - Catch ValueError → raise HTTPException 422 with the error message
            - Catch LLMProviderError → raise HTTPException 502 with a safe message
            - Catch any other Exception → log it, raise HTTPException 500
            - Return the result on success

        Args:
            request: Validated QARequest from the router.

        Returns:
            QAResponse.

        Raises:
            HTTPException 422: If input validation fails inside the service.
            HTTPException 502: If the LLM provider call fails.
            HTTPException 500: For any unexpected error.
        """
        raise NotImplementedError
