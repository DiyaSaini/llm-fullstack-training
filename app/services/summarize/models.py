"""
Internal dataclasses for the Summarize service.

These are used exclusively within the service layer for passing
data between methods. They never cross the HTTP boundary.
Pydantic is only used at the schema (HTTP) layer.
"""

from dataclasses import dataclass


@dataclass
class SummarizeInput:
    """
    Validated, normalised input ready for prompt construction.

    TODO (Associate 1):
        Populate this from validate_input() in your service.
        Add or remove fields as your implementation requires.
    """

    text: str
    max_length: int | None = None
