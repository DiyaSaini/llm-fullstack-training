"""
Keywords controller.

ASSOCIATE 3 — implement the handle() method below.

The controller is responsible for:
    - Receiving the validated request from the router
    - Calling the pipeline
    - Translating exceptions into appropriate HTTP responses
    - Returning the response object

It does NOT contain business logic. That lives in the service.
"""

from fastapi import HTTPException

from app.api.v1.schemas.requests.keywords import KeywordsRequest
from app.api.v1.schemas.responses.keywords import KeywordsResponse
from app.core.pipeline.keywords_pipeline import KeywordsPipeline
from app.logging import get_logger
from app.providers.llm_provider import LLMProviderError

logger = get_logger(__name__)


class KeywordsController:
    """Handles HTTP concerns for the /keywords endpoint."""

    def __init__(self, pipeline: KeywordsPipeline) -> None:
        self.pipeline = pipeline

    def handle(self, request: KeywordsRequest) -> KeywordsResponse:
        """
        Process a keywords request.

        TODO:
            - Call self.pipeline.execute(request)
            - Catch ValueError → raise HTTPException 422 with the error message
            - Catch LLMProviderError → raise HTTPException 502 with a safe message
            - Catch any other Exception → log it, raise HTTPException 500
            - Return the result on success

        Args:
            request: Validated KeywordsRequest from the router.

        Returns:
            KeywordsResponse.

        Raises:
            HTTPException 422: If input validation fails inside the service.
            HTTPException 502: If the LLM provider call fails.
            HTTPException 500: For any unexpected error.
        """
        try:
            return self.pipeline.execute(request)

        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e)) from e

        except LLMProviderError as e:
            raise HTTPException(
                status_code=502, detail="Keyword extraction provider failed."
            ) from e

        except Exception as e:
            logger.exception("Unexpected error in keywords controller")
            raise HTTPException(status_code=500, detail="Internal server error") from e
