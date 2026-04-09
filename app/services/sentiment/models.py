"""
Internal dataclasses for the Sentiment service.

Used exclusively within the service layer.
Never cross the HTTP boundary.
"""

from dataclasses import dataclass


@dataclass
class SentimentInput:
    """
    Validated, normalised input ready for prompt construction.

    TODO (Associate 4):
        Populate this from validate_input() in your service.
        Add or remove fields as your implementation requires.
    """

    text: str
