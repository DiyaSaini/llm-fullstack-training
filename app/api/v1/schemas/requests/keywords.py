"""
Keywords request schema.

TODO (Associate 3):
    - Add field validators if needed
"""

from pydantic import BaseModel, Field, field_validator


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

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Text cannot be empty")
        return value
