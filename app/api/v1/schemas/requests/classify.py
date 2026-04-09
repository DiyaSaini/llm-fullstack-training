"""
Classify request schema.

TODO (Associate 2):
    - Add field validators if needed
    - Consider validation for categories list items
"""

from pydantic import BaseModel, Field


class ClassifyRequest(BaseModel):
    """Payload for POST /api/v1/classify."""

    text: str = Field(
        ...,
        min_length=5,
        description="The text to classify.",
        examples=["The new iPhone features a revolutionary camera system..."],
    )
    categories: list[str] | None = Field(
        default=None,
        description=(
            "Optional list of target categories. "
            "If omitted, the model chooses the most appropriate category freely."
        ),
        examples=[["technology", "sports", "politics", "entertainment"]],
    )
