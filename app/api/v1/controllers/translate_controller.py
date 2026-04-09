"""
Translate controller.

ASSOCIATE 7 — implement the handle() method below.

The controller is responsible for:
    - Receiving the validated request from the router
    - Calling the pipeline
    - Translating exceptions into appropriate HTTP responses
    - Returning the response object

It does NOT contain business logic. That lives in the service.
"""

from app.api.v1.schemas.requests.translate import TranslateRequest
from app.api.v1.schemas.responses.translate import TranslateResponse
from app.core.pipeline.translate_pipeline import TranslatePipeline
from app.logging import get_logger

logger = get_logger(__name__)


class TranslateController:
    """Handles HTTP concerns for the /translate endpoint."""

    def __init__(self, pipeline: TranslatePipeline) -> None:
        self.pipeline = pipeline

    def handle(self, request: TranslateRequest) -> TranslateResponse:
        """
        Process a translate request.

        TODO:
            - Call self.pipeline.execute(request)
            - Catch ValueError → raise HTTPException 422 with the error message
            - Catch LLMProviderError → raise HTTPException 502 with a safe message
            - Catch any other Exception → log it, raise HTTPException 500
            - Return the result on success

        Args:
            request: Validated TranslateRequest from the router.

        Returns:
            TranslateResponse.

        Raises:
            HTTPException 422: If input validation fails inside the service.
            HTTPException 502: If the LLM provider call fails.
            HTTPException 500: For any unexpected error.
        """
        raise NotImplementedError
