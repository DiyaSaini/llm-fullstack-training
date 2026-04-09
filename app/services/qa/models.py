"""
Internal dataclasses for the QA service.

Used exclusively within the service layer.
Never cross the HTTP boundary.
"""

from dataclasses import dataclass


@dataclass
class QAInput:
    """
    Validated, normalised input ready for prompt construction.

    TODO (Associate 5):
        Populate this from validate_input() in your service.
        Add or remove fields as your implementation requires.
    """

    context: str
    question: str
