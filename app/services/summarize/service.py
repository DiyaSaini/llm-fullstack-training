"""
Summarize service — concrete implementation.

ASSOCIATE 1 — this is your primary file to implement.

You must implement all three methods below.
Read summarize_interface.py for the full contract and expected
JSON shape that your build_prompt must instruct the LLM to return.

Steps to get started:
    1. Read app/core/interfaces/summarize_interface.py carefully
    2. Read app/core/pipeline/summarize_pipeline.py to understand call order
    3. Read app/services/summarize/models.py for the SummarizeInput dataclass
    4. Read app/api/v1/schemas/requests/summarize.py for incoming request shape
    5. Read app/api/v1/schemas/responses/summarize.py for expected response shape
    6. Implement each method below
    7. Run your tests: pytest tests/test_summarize.py -v
    8. Run your script: python scripts/run_summarize.py --text "Your text here"
"""

from app.api.v1.schemas.requests.summarize import SummarizeRequest
from app.api.v1.schemas.responses.summarize import SummarizeResponse
from app.core.interfaces.summarize_interface import SummarizeServiceInterface
from app.logging import get_logger
from app.providers.llm_provider import BaseLLMProvider
from app.services.summarize.models import SummarizeInput

logger = get_logger(__name__)


class SummarizeService(SummarizeServiceInterface):
    """Concrete implementation of the summarization service."""

    def __init__(self, provider: BaseLLMProvider) -> None:
        super().__init__(provider)

    def validate_input(self, request: SummarizeRequest) -> SummarizeInput:
        """
        Validate and normalise the summarize request.

        TODO:
            - Strip leading/trailing whitespace from text
            - Raise ValueError if text is empty after stripping
            - Return a populated SummarizeInput dataclass

        Args:
            request: Incoming SummarizeRequest.

        Returns:
            SummarizeInput dataclass.

        Raises:
            ValueError: If text is empty after stripping.
        """
        raise NotImplementedError

    def build_prompt(self, validated_input: SummarizeInput) -> str:
        """
        Construct the summarization prompt string.

        TODO:
            - Write a clear prompt instructing the LLM to summarize the text
            - If max_length is set, include it as a constraint in the prompt
            - Instruct the LLM to respond ONLY with valid JSON, no markdown fences
            - The JSON must contain: short_summary, detailed_summary, key_points
            - Include the text from validated_input in the prompt

        Args:
            validated_input: Output of validate_input().

        Returns:
            Fully constructed prompt string.
        """
        raise NotImplementedError

    def parse_response(self, raw_response: str) -> SummarizeResponse:
        """
        Parse the raw LLM JSON response into a SummarizeResponse.

        TODO:
            - Strip any accidental markdown fences (```json ... ```) if present
            - Parse the string as JSON using json.loads()
            - Construct and return a SummarizeResponse from the parsed dict
            - Raise ValueError with a clear message if parsing fails

        Args:
            raw_response: Raw string returned by the LLM.

        Returns:
            Populated SummarizeResponse.

        Raises:
            ValueError: If the response is not valid JSON or fields are missing.
        """
        raise NotImplementedError
