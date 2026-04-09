"""
Summarize request schema.

TODO (Associate 1):
    - Add any additional fields you think are useful
    - Add field validators using @field_validator if needed
"""

from pydantic import BaseModel, Field


class SummarizeRequest(BaseModel):
    """Payload for POST /api/v1/summarize."""

    text: str = Field(
        ...,
        min_length=10,
        description="The text to summarize. Must be at least 10 characters.",
        examples=["Artificial intelligence is transforming industries worldwide..."],
    )
    max_length: int | None = Field(
        default=None,
        ge=50,
        le=1000,
        description="Optional maximum word count for the summary.",
    )
