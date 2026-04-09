"""
Internal dataclasses for the Classify service.

Used exclusively within the service layer.
Never cross the HTTP boundary.
"""

from dataclasses import dataclass, field


@dataclass
class ClassifyInput:
    """
    Validated, normalised input ready for prompt construction.

    TODO (Associate 2):
        Populate this from validate_input() in your service.
        Add or remove fields as your implementation requires.
    """

    text: str
    categories: list[str] = field(default_factory=list)
