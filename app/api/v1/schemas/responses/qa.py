"""
Q&A response schema.

TODO (Associate 5):
    - Ensure field names match what your build_prompt instructs the LLM to return
"""

from pydantic import BaseModel, Field


class QAResponse(BaseModel):
    """Response body for POST /api/v1/qa."""

    answer: str = Field(
        ...,
        description="The answer derived strictly from the provided context.",
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score for the answer.",
    )
    is_answerable: bool = Field(
        ...,
        description="False if the answer cannot be found in the provided context.",
    )
