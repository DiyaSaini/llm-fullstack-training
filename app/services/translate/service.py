"""
Translate service — concrete implementation.

ASSOCIATE 7 — this is your primary file to implement.

Steps to get started:
    1. Read app/core/interfaces/translate_interface.py carefully
    2. Read app/core/pipeline/translate_pipeline.py to understand call order
    3. Read app/services/translate/models.py for the TranslateInput dataclass
    4. Read app/api/v1/schemas/requests/translate.py for incoming request shape
    5. Read app/api/v1/schemas/responses/translate.py for expected response shape
    6. Implement each method below
    7. Run your tests: pytest tests/test_translate.py -v
    8. Run your script: python scripts/run_translate.py --text "..." --target-language "French"
"""

from app.api.v1.schemas.requests.translate import TranslateRequest
from app.api.v1.schemas.responses.translate import TranslateResponse
from app.core.interfaces.translate_interface import TranslateServiceInterface
from app.logging import get_logger
from app.providers.llm_provider import BaseLLMProvider
from app.services.translate.models import TranslateInput

logger = get_logger(__name__)


class TranslateService(TranslateServiceInterface):
    """Concrete implementation of the translation service."""

    def __init__(self, provider: BaseLLMProvider) -> None:
        super().__init__(provider)

    def validate_input(self, request: TranslateRequest) -> TranslateInput:
        """
        Validate and normalise the translate request.

        TODO:
            - Strip whitespace from text and target_language
            - Raise ValueError if text is empty after stripping
            - Raise ValueError if target_language is empty after stripping
            - Return a populated TranslateInput dataclass

        Args:
            request: Incoming TranslateRequest.

        Returns:
            TranslateInput dataclass.

        Raises:
            ValueError: If text or target_language is empty after stripping.
        """
        raise NotImplementedError

    def build_prompt(self, validated_input: TranslateInput) -> str:
        """
        Construct the translation prompt.

        TODO:
            - Instruct the LLM to detect the source language automatically
            - Instruct it to translate to target_language
            - Instruct LLM to respond ONLY with valid JSON, no markdown fences
            - JSON must contain:
                detected_language, target_language, translated_text, confidence

        Args:
            validated_input: Output of validate_input().

        Returns:
            Fully constructed prompt string.
        """
        raise NotImplementedError

    def parse_response(self, raw_response: str) -> TranslateResponse:
        """
        Parse the raw LLM JSON response into a TranslateResponse.

        TODO:
            - Strip any accidental markdown fences if present
            - Parse the string as JSON
            - Construct and return a TranslateResponse
            - Raise ValueError if parsing fails or required fields are missing

        Args:
            raw_response: Raw string returned by the LLM.

        Returns:
            Populated TranslateResponse.

        Raises:
            ValueError: If the response cannot be parsed.
        """
        raise NotImplementedError
