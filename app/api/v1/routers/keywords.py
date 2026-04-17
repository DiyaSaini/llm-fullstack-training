"""
Keywords router.

ASSOCIATE 3 — implement the route below.

The router's only job is to declare the endpoint path, HTTP method,
and response model, then delegate immediately to the controller.
No business logic lives here.
"""

from fastapi import APIRouter, Depends, status

from app.api.v1.controllers.keywords_controller import KeywordsController
from app.api.v1.deps import get_keywords_pipeline
from app.api.v1.schemas.requests.keywords import KeywordsRequest
from app.api.v1.schemas.responses.keywords import KeywordsResponse
from app.core.pipeline.keywords_pipeline import KeywordsPipeline

router = APIRouter()


@router.post(
    "/keywords",
    response_model=KeywordsResponse,
    status_code=status.HTTP_200_OK,
    summary="Extract keywords",
    description="Extracts and ranks keywords by relevance from the provided text.",
)
async def keywords(
    request: KeywordsRequest,
    pipeline: KeywordsPipeline = Depends(get_keywords_pipeline),
) -> KeywordsResponse:
    """
    TODO (Associate 3):
        - Instantiate KeywordsController with the injected pipeline
        - Call controller.handle(request)
        - Return the result
        - Let HTTPException propagate naturally — do not catch it here
    """
    controller = KeywordsController(pipeline=pipeline)
    result = controller.handle(request)
    return result
