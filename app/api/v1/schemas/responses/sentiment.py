"""
Sentiment response schema.

TODO (Associate 4):
    - Ensure field names match what your build_prompt instructs the LLM to return
"""

from typing import Literal

from pydantic import BaseModel, Field


class SentimentResponse(BaseModel):
    """Response body for POST /api/v1/sentiment."""

    sentiment: Literal["positive", "negative", "neutral", "mixed"] = Field(
        ...,
        description="The overall sentiment classification.",
    )
    score: float = Field(
        ...,
        ge=-1.0,
        le=1.0,
        description="Sentiment score: -1.0 (very negative) to 1.0 (very positive).",
    )
    reasoning: str = Field(
        ...,
        description="Explanation of the sentiment classification.",
    )
    emotions: list[str] = Field(
        default_factory=list,
        description="List of detected emotions (e.g. joy, anger, sadness).",
    )
