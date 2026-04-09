"""
Classify router.

ASSOCIATE 2 — implement the route below.

The router's only job is to declare the endpoint path, HTTP method,
and response model, then delegate immediately to the controller.
No business logic lives here.
"""

from fastapi import APIRouter, Depends, status

from app.api.v1.deps import get_classify_pipeline
from app.api.v1.schemas.requests.classify import ClassifyRequest
from app.api.v1.schemas.responses.classify import ClassifyResponse
from app.core.pipeline.classify_pipeline import ClassifyPipeline

router = APIRouter()


@router.post(
    "/classify",
    response_model=ClassifyResponse,
    status_code=status.HTTP_200_OK,
    summary="Classify text",
    description="Classifies text into a category with a confidence score and reasoning.",
)
async def classify(
    request: ClassifyRequest,
    pipeline: ClassifyPipeline = Depends(get_classify_pipeline),
) -> ClassifyResponse:
    """
    TODO (Associate 2):
        - Instantiate ClassifyController with the injected pipeline
        - Call controller.handle(request)
        - Return the result
        - Let HTTPException propagate naturally — do not catch it here
    """
    raise NotImplementedError
