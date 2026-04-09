"""Paraphrase service interface."""

from abc import abstractmethod

from app.api.v1.schemas.requests.paraphrase import ParaphraseRequest
from app.api.v1.schemas.responses.paraphrase import ParaphraseResponse
from app.core.interfaces.base_service import BaseService
from app.services.paraphrase.models import ParaphraseInput


class ParaphraseServiceInterface(BaseService):
    """
    Contract for the paraphrase service.

    Rewrites the input text in one or more requested tones/styles
    without changing the meaning.

    Pipeline call order:
        1. validate_input(request)  → ParaphraseInput
        2. build_prompt(input)      → str
        3. call_llm(prompt)         → str
        4. parse_response(raw)      → ParaphraseResponse
    """

    @abstractmethod
    def validate_input(self, request: ParaphraseRequest) -> ParaphraseInput:
        """
        Validate the paraphrase request.

        Args:
            request: Pydantic request with `text` and `tones` list.
                     Valid tones: formal, casual, simple, creative, professional.

        Returns:
            ParaphraseInput dataclass.

        Raises:
            ValueError: If text is empty or an unrecognised tone is requested.
        """
        raise NotImplementedError

    @abstractmethod
    def build_prompt(self, validated_input: ParaphraseInput) -> str:
        """
        Build the paraphrase prompt.

        The prompt must instruct the LLM to return JSON:
            {
                "paraphrases": [
                    {"tone": "formal", "text": "..."},
                    {"tone": "casual", "text": "..."}
                ]
            }

        One entry per requested tone.

        Args:
            validated_input: Output of validate_input().

        Returns:
            Prompt string.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_response(self, raw_response: str) -> ParaphraseResponse:
        """
        Parse JSON response into ParaphraseResponse.

        Raises:
            ValueError: If JSON is malformed or paraphrases list is missing.
        """
        raise NotImplementedError
