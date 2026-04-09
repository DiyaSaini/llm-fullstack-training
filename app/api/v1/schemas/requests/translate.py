"""
Translate request schema.

TODO (Associate 7):
    - Add field validators if needed
"""

from pydantic import BaseModel, Field


class TranslateRequest(BaseModel):
    """Payload for POST /api/v1/translate."""

    text: str = Field(
        ...,
        min_length=2,
        description="The text to translate.",
        examples=["Bonjour, comment allez-vous?"],
    )
    target_language: str = Field(
        ...,
        min_length=2,
        description=(
            "Target language name or ISO 639-1 code. "
            "Examples: 'French', 'fr', 'Spanish', 'es', 'Hindi', 'hi'."
        ),
        examples=["English"],
    )
