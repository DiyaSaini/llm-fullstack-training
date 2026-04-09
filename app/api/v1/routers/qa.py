"""
Qa router.

ASSOCIATE 5 — implement the route below.

The router's only job is to declare the endpoint path, HTTP method,
and response model, then delegate immediately to the controller.
No business logic lives here.
"""

from fastapi import APIRouter, Depends, status

from app.api.v1.deps import get_qa_pipeline
from app.api.v1.schemas.requests.qa import QARequest
from app.api.v1.schemas.responses.qa import QAResponse
from app.core.pipeline.qa_pipeline import QAPipeline

router = APIRouter()


@router.post(
    "/qa",
    response_model=QAResponse,
    status_code=status.HTTP_200_OK,
    summary="Answer a question from context",
    description="Answers a question strictly from the provided context passage.",
)
async def qa(
    request: QARequest,
    pipeline: QAPipeline = Depends(get_qa_pipeline),
) -> QAResponse:
    """
    TODO (Associate 5):
        - Instantiate QaController with the injected pipeline
        - Call controller.handle(request)
        - Return the result
        - Let HTTPException propagate naturally — do not catch it here
    """
    raise NotImplementedError
