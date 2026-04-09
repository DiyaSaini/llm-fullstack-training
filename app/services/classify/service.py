"""
Classify service — concrete implementation.

ASSOCIATE 2 — this is your primary file to implement.

You must implement all three methods below.
Read classify_interface.py for the full contract and expected
JSON shape that your build_prompt must instruct the LLM to return.

Steps to get started:
    1. Read app/core/interfaces/classify_interface.py carefully
    2. Read app/core/pipeline/classify_pipeline.py to understand call order
    3. Read app/services/classify/models.py for the ClassifyInput dataclass
    4. Read app/api/v1/schemas/requests/classify.py for incoming request shape
    5. Read app/api/v1/schemas/responses/classify.py for expected response shape
    6. Implement each method below
    7. Run your tests: pytest tests/test_classify.py -v
    8. Run your script: python scripts/run_classify.py --text "Your text here"
"""

from app.api.v1.schemas.requests.classify import ClassifyRequest
from app.api.v1.schemas.responses.classify import ClassifyResponse
from app.core.interfaces.classify_interface import ClassifyServiceInterface
from app.logging import get_logger
from app.providers.llm_provider import BaseLLMProvider
from app.services.classify.models import ClassifyInput

logger = get_logger(__name__)


class ClassifyService(ClassifyServiceInterface):
    """Concrete implementation of the text classification service."""

    def __init__(self, provider: BaseLLMProvider) -> None:
        super().__init__(provider)

    def validate_input(self, request: ClassifyRequest) -> ClassifyInput:
        """
        Validate and normalise the classify request.

        TODO:
            - Strip whitespace from text
            - Raise ValueError if text is empty after stripping
            - Normalise categories to lowercase if provided
            - Return a populated ClassifyInput dataclass

        Args:
            request: Incoming ClassifyRequest.

        Returns:
            ClassifyInput dataclass.

        Raises:
            ValueError: If text is empty after stripping.
        """
        raise NotImplementedError

    def build_prompt(self, validated_input: ClassifyInput) -> str:
        """
        Construct the classification prompt string.

        TODO:
            - If categories are provided, instruct LLM to pick from that list only
            - If categories are empty, instruct LLM to choose the best category freely
            - Instruct the LLM to respond ONLY with valid JSON, no markdown fences
            - The JSON must contain: category, confidence (0.0-1.0), reasoning
            - Include the text from validated_input in the prompt

        Args:
            validated_input: Output of validate_input().

        Returns:
            Fully constructed prompt string.
        """
        raise NotImplementedError

    def parse_response(self, raw_response: str) -> ClassifyResponse:
        """
        Parse the raw LLM JSON response into a ClassifyResponse.

        TODO:
            - Strip any accidental markdown fences if present
            - Parse the string as JSON
            - Construct and return a ClassifyResponse
            - Raise ValueError with a clear message if parsing fails

        Args:
            raw_response: Raw string returned by the LLM.

        Returns:
            Populated ClassifyResponse.

        Raises:
            ValueError: If the response is not valid JSON or fields are missing.
        """
        raise NotImplementedError
