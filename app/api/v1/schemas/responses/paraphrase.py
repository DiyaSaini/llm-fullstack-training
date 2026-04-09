"""
Paraphrase response schema.

TODO (Associate 6):
    - Ensure field names match what your build_prompt instructs the LLM to return
"""

from pydantic import BaseModel, Field


class ParaphraseVariant(BaseModel):
    """A single paraphrased version in a specific tone."""

    tone: str = Field(..., description="The tone applied to this variant.")
    text: str = Field(..., description="The paraphrased text in this tone.")


class ParaphraseResponse(BaseModel):
    """Response body for POST /api/v1/paraphrase."""

    paraphrases: list[ParaphraseVariant] = Field(
        ...,
        description="One paraphrased version per requested tone.",
        min_length=1,
    )
