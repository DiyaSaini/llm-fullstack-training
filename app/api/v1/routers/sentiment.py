"""
Sentiment router.

ASSOCIATE 4 — implement the route below.

The router's only job is to declare the endpoint path, HTTP method,
and response model, then delegate immediately to the controller.
No business logic lives here.
"""

from fastapi import APIRouter, Depends, status

from app.api.v1.deps import get_sentiment_pipeline
from app.api.v1.schemas.requests.sentiment import SentimentRequest
from app.api.v1.schemas.responses.sentiment import SentimentResponse
from app.core.pipeline.sentiment_pipeline import SentimentPipeline

router = APIRouter()


@router.post(
    "/sentiment",
    response_model=SentimentResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyse sentiment",
    description="Analyses the sentiment of the provided text.",
)
async def sentiment(
    request: SentimentRequest,
    pipeline: SentimentPipeline = Depends(get_sentiment_pipeline),
) -> SentimentResponse:
    """
    TODO (Associate 4):
        - Instantiate SentimentController with the injected pipeline
        - Call controller.handle(request)
        - Return the result
        - Let HTTPException propagate naturally — do not catch it here
    """
    raise NotImplementedError
