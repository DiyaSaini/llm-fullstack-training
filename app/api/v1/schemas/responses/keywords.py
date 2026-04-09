"""
Keywords response schema.

TODO (Associate 3):
    - Ensure field names match what your build_prompt instructs the LLM to return
"""

from pydantic import BaseModel, Field


class Keyword(BaseModel):
    """A single extracted keyword with its relevance score."""

    word: str = Field(..., description="The keyword or key phrase.")
    relevance_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Relevance score between 0.0 (low) and 1.0 (high).",
    )


class KeywordsResponse(BaseModel):
    """Response body for POST /api/v1/keywords."""

    keywords: list[Keyword] = Field(
        ...,
        description="List of extracted keywords ordered by relevance descending.",
        min_length=1,
    )
