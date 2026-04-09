"""
Sentiment request schema.

TODO (Associate 4):
    - Add field validators if needed
"""

from pydantic import BaseModel, Field


class SentimentRequest(BaseModel):
    """Payload for POST /api/v1/sentiment."""

    text: str = Field(
        ...,
        min_length=5,
        description="The text to analyse for sentiment.",
        examples=[
            "I absolutely loved the movie! The acting was superb and the plot kept me hooked."
        ],
    )
