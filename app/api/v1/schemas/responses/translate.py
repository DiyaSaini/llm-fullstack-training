"""
Translate response schema.

TODO (Associate 7):
    - Ensure field names match what your build_prompt instructs the LLM to return
"""

from pydantic import BaseModel, Field


class TranslateResponse(BaseModel):
    """Response body for POST /api/v1/translate."""

    detected_language: str = Field(
        ...,
        description="The language detected in the input text.",
    )
    target_language: str = Field(
        ...,
        description="The language the text was translated into.",
    )
    translated_text: str = Field(
        ...,
        description="The translated text.",
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score for the translation quality.",
    )
