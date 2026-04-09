"""
Paraphrase request schema.

TODO (Associate 6):
    - Add a @field_validator to ensure all requested tones are valid
    - Valid tones: formal, casual, simple, creative, professional
"""

from pydantic import BaseModel, Field

VALID_TONES = {"formal", "casual", "simple", "creative", "professional"}


class ParaphraseRequest(BaseModel):
    """Payload for POST /api/v1/paraphrase."""

    text: str = Field(
        ...,
        min_length=10,
        description="The text to paraphrase.",
        examples=[
            "The utilisation of advanced computational methodologies has precipitated significant transformations."
        ],
    )
    tones: list[str] = Field(
        default=["formal", "casual"],
        description=(
            f"List of tones to paraphrase into. "
            f"Valid values: {sorted(VALID_TONES)}. "
            f"At least one tone required."
        ),
        min_length=1,
    )
