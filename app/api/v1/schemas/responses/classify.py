"""
Classify response schema.

TODO (Associate 2):
    - Add any additional fields your service produces
    - Ensure field names match what your build_prompt instructs the LLM to return
"""

from pydantic import BaseModel, Field


class ClassifyResponse(BaseModel):
    """Response body for POST /api/v1/classify."""

    category: str = Field(
        ...,
        description="The predicted category label.",
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0.0 and 1.0.",
    )
    reasoning: str = Field(
        ...,
        description="Brief explanation of why this category was chosen.",
    )
