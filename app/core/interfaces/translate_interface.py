"""Translation service interface."""

from abc import abstractmethod

from app.api.v1.schemas.requests.translate import TranslateRequest
from app.api.v1.schemas.responses.translate import TranslateResponse
from app.core.interfaces.base_service import BaseService
from app.services.translate.models import TranslateInput


class TranslateServiceInterface(BaseService):
    """
    Contract for the translation service.

    Detects the source language automatically and translates
    the text to the requested target language.

    Pipeline call order:
        1. validate_input(request)  → TranslateInput
        2. build_prompt(input)      → str
        3. call_llm(prompt)         → str
        4. parse_response(raw)      → TranslateResponse
    """

    @abstractmethod
    def validate_input(self, request: TranslateRequest) -> TranslateInput:
        """
        Validate the translate request.

        Args:
            request: Pydantic request with `text` and `target_language`.
                     `target_language` is a language name or ISO 639-1 code (e.g. "French", "fr").

        Returns:
            TranslateInput dataclass.

        Raises:
            ValueError: If text is empty or target_language is missing.
        """
        raise NotImplementedError

    @abstractmethod
    def build_prompt(self, validated_input: TranslateInput) -> str:
        """
        Build the translation prompt.

        The prompt must instruct the LLM to:
            - Auto-detect the source language
            - Translate to target_language
            - Return JSON:
                {
                    "detected_language": "...",
                    "target_language": "...",
                    "translated_text": "...",
                    "confidence": 0.0-1.0
                }

        Args:
            validated_input: Output of validate_input().

        Returns:
            Prompt string.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_response(self, raw_response: str) -> TranslateResponse:
        """
        Parse JSON response into TranslateResponse.

        Raises:
            ValueError: If JSON is malformed or translated_text is missing.
        """
        raise NotImplementedError
