"""
Translate router.

ASSOCIATE 7 — implement the route below.

The router's only job is to declare the endpoint path, HTTP method,
and response model, then delegate immediately to the controller.
No business logic lives here.
"""

from fastapi import APIRouter, Depends, status

from app.api.v1.deps import get_translate_pipeline
from app.api.v1.schemas.requests.translate import TranslateRequest
from app.api.v1.schemas.responses.translate import TranslateResponse
from app.core.pipeline.translate_pipeline import TranslatePipeline

router = APIRouter()


@router.post(
    "/translate",
    response_model=TranslateResponse,
    status_code=status.HTTP_200_OK,
    summary="Translate text",
    description="Detects the source language and translates text to the target language.",
)
async def translate(
    request: TranslateRequest,
    pipeline: TranslatePipeline = Depends(get_translate_pipeline),
) -> TranslateResponse:
    """
    TODO (Associate 7):
        - Instantiate TranslateController with the injected pipeline
        - Call controller.handle(request)
        - Return the result
        - Let HTTPException propagate naturally — do not catch it here
    """
    raise NotImplementedError
