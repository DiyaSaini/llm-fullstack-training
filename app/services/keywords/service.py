"""
Keywords service — concrete implementation.

ASSOCIATE 3 — this is your primary file to implement.

Steps to get started:
    1. Read app/core/interfaces/keywords_interface.py carefully
    2. Read app/core/pipeline/keywords_pipeline.py to understand call order
    3. Read app/services/keywords/models.py for the KeywordsInput dataclass
    4. Read app/api/v1/schemas/requests/keywords.py for incoming request shape
    5. Read app/api/v1/schemas/responses/keywords.py for expected response shape
    6. Implement each method below
    7. Run your tests: pytest tests/test_keywords.py -v
    8. Run your script: python scripts/run_keywords.py --text "Your text here"
"""

from app.api.v1.schemas.requests.keywords import KeywordsRequest
from app.api.v1.schemas.responses.keywords import KeywordsResponse
from app.core.interfaces.keywords_interface import KeywordsServiceInterface
from app.logging import get_logger
from app.providers.llm_provider import BaseLLMProvider
from app.services.keywords.models import KeywordsInput

logger = get_logger(__name__)


class KeywordsService(KeywordsServiceInterface):
    """Concrete implementation of the keyword extraction service."""

    def __init__(self, provider: BaseLLMProvider) -> None:
        super().__init__(provider)

    def validate_input(self, request: KeywordsRequest) -> KeywordsInput:
        """
        Validate and normalise the keywords request.

        TODO:
            - Strip whitespace from text
            - Raise ValueError if text is empty after stripping
            - Ensure max_keywords is between 1 and 20 (it is validated by Pydantic,
              but add a defensive check here too)
            - Return a populated KeywordsInput dataclass

        Args:
            request: Incoming KeywordsRequest.

        Returns:
            KeywordsInput dataclass.

        Raises:
            ValueError: If text is empty or max_keywords is out of range.
        """
        raise NotImplementedError

    def build_prompt(self, validated_input: KeywordsInput) -> str:
        """
        Construct the keyword extraction prompt.

        TODO:
            - Instruct the LLM to extract up to max_keywords keywords
            - Ask for keywords ordered by relevance score descending
            - Instruct LLM to respond ONLY with valid JSON, no markdown fences
            - The JSON must contain: keywords (list of {word, relevance_score})
            - Include the text from validated_input in the prompt

        Args:
            validated_input: Output of validate_input().

        Returns:
            Fully constructed prompt string.
        """
        raise NotImplementedError

    def parse_response(self, raw_response: str) -> KeywordsResponse:
        """
        Parse the raw LLM JSON response into a KeywordsResponse.

        TODO:
            - Strip any accidental markdown fences if present
            - Parse the string as JSON
            - Construct Keyword objects from the list
            - Construct and return a KeywordsResponse
            - Raise ValueError if parsing fails or keywords list is empty

        Args:
            raw_response: Raw string returned by the LLM.

        Returns:
            Populated KeywordsResponse.

        Raises:
            ValueError: If the response is not valid JSON or keywords are missing.
        """
        raise NotImplementedError
