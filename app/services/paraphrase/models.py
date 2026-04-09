"""
Internal dataclasses for the Paraphrase service.

Used exclusively within the service layer.
Never cross the HTTP boundary.
"""

from dataclasses import dataclass, field


@dataclass
class ParaphraseInput:
    """
    Validated, normalised input ready for prompt construction.

    TODO (Associate 6):
        Populate this from validate_input() in your service.
        Add or remove fields as your implementation requires.
    """

    text: str
    tones: list[str] = field(default_factory=lambda: ["formal", "casual"])
