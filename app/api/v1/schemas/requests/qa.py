"""
Q&A request schema.

TODO (Associate 5):
    - Add field validators if needed
"""

from pydantic import BaseModel, Field


class QARequest(BaseModel):
    """Payload for POST /api/v1/qa."""

    context: str = Field(
        ...,
        min_length=20,
        description="The context passage the question should be answered from.",
        examples=[
            "The Python programming language was created by Guido van Rossum and first released in 1991..."
        ],
    )
    question: str = Field(
        ...,
        min_length=5,
        description="The question to answer based strictly on the provided context.",
        examples=["Who created Python?"],
    )
