"""
Summarize response schema.

TODO (Associate 1):
    - Add any additional response fields your service produces
    - Ensure field names match exactly what your build_prompt instructs the LLM to return
"""

from pydantic import BaseModel, Field


class SummarizeResponse(BaseModel):
    """Response body for POST /api/v1/summarize."""

    short_summary: str = Field(
        ...,
        description="A concise summary in 1-2 sentences.",
    )
    detailed_summary: str = Field(
        ...,
        description="A comprehensive paragraph-length summary.",
    )
    key_points: list[str] = Field(
        ...,
        description="3 to 5 key points extracted from the text.",
        min_length=1,
    )
