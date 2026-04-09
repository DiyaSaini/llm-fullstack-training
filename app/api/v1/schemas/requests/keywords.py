"""
Keywords request schema.

TODO (Associate 3):
    - Add field validators if needed
"""

from pydantic import BaseModel, Field


class KeywordsRequest(BaseModel):
    """Payload for POST /api/v1/keywords."""

    text: str = Field(
        ...,
        min_length=10,
        description="The text to extract keywords from.",
        examples=[
            "Climate change is accelerating the frequency of extreme weather events..."
        ],
    )
    max_keywords: int = Field(
        default=10,
        ge=1,
        le=20,
        description="Maximum number of keywords to return. Defaults to 10.",
    )
