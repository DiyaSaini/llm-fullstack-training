"""
Internal dataclasses for the Keywords service.

Used exclusively within the service layer.
Never cross the HTTP boundary.
"""

from dataclasses import dataclass


@dataclass
class KeywordsInput:
    """
    Validated, normalised input ready for prompt construction.

    TODO (Associate 3):
        Populate this from validate_input() in your service.
        Add or remove fields as your implementation requires.
    """

    text: str
    max_keywords: int = 10
