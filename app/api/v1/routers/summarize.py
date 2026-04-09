"""
Summarize router.

ASSOCIATE 1 — implement the route below.

The router's only job is to declare the endpoint path, HTTP method,
and response model, then delegate immediately to the controller.
No business logic lives here.
"""

from fastapi import APIRouter, Depends, status

from app.api.v1.deps import get_summarize_pipeline
from app.api.v1.schemas.requests.summarize import SummarizeRequest
from app.api.v1.schemas.responses.summarize import SummarizeResponse
from app.core.pipeline.summarize_pipeline import SummarizePipeline

router = APIRouter()


@router.post(
    "/summarize",
    response_model=SummarizeResponse,
    status_code=status.HTTP_200_OK,
    summary="Summarize text",
    description=(
        "Accepts a block of text and returns a short summary, "
        "a detailed summary, and a list of key points."
    ),
)
async def summarize(
    request: SummarizeRequest,
    pipeline: SummarizePipeline = Depends(get_summarize_pipeline),
) -> SummarizeResponse:
    """
    TODO (Associate 1):
        - Instantiate SummarizeController with the injected pipeline
        - Call controller.handle(request)
        - Return the result
        - Let HTTPException propagate naturally — do not catch it here
    """
    raise NotImplementedError
