"""
Internal dataclasses for the Translate service.

Used exclusively within the service layer.
Never cross the HTTP boundary.
"""

from dataclasses import dataclass


@dataclass
class TranslateInput:
    """
    Validated, normalised input ready for prompt construction.

    TODO (Associate 7):
        Populate this from validate_input() in your service.
        Add or remove fields as your implementation requires.
    """

    text: str
    target_language: str
