"""
Paraphrase router.

ASSOCIATE 6 — implement the route below.

The router's only job is to declare the endpoint path, HTTP method,
and response model, then delegate immediately to the controller.
No business logic lives here.
"""

from fastapi import APIRouter, Depends, status

from app.api.v1.deps import get_paraphrase_pipeline
from app.api.v1.schemas.requests.paraphrase import ParaphraseRequest
from app.api.v1.schemas.responses.paraphrase import ParaphraseResponse
from app.core.pipeline.paraphrase_pipeline import ParaphrasePipeline

router = APIRouter()


@router.post(
    "/paraphrase",
    response_model=ParaphraseResponse,
    status_code=status.HTTP_200_OK,
    summary="Paraphrase text",
    description="Rewrites text in one or more requested tones.",
)
async def paraphrase(
    request: ParaphraseRequest,
    pipeline: ParaphrasePipeline = Depends(get_paraphrase_pipeline),
) -> ParaphraseResponse:
    """
    TODO (Associate 6):
        - Instantiate ParaphraseController with the injected pipeline
        - Call controller.handle(request)
        - Return the result
        - Let HTTPException propagate naturally — do not catch it here
    """
    raise NotImplementedError
