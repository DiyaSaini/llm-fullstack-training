"""
QA service — concrete implementation.

ASSOCIATE 5 — this is your primary file to implement.

Steps to get started:
    1. Read app/core/interfaces/qa_interface.py carefully
    2. Read app/core/pipeline/qa_pipeline.py to understand call order
    3. Read app/services/qa/models.py for the QAInput dataclass
    4. Read app/api/v1/schemas/requests/qa.py for incoming request shape
    5. Read app/api/v1/schemas/responses/qa.py for expected response shape
    6. Implement each method below
    7. Run your tests: pytest tests/test_qa.py -v
    8. Run your script: python scripts/run_qa.py --context "..." --question "..."
"""

from app.api.v1.schemas.requests.qa import QARequest
from app.api.v1.schemas.responses.qa import QAResponse
from app.core.interfaces.qa_interface import QAServiceInterface
from app.logging import get_logger
from app.providers.llm_provider import BaseLLMProvider
from app.services.qa.models import QAInput

logger = get_logger(__name__)


class QAService(QAServiceInterface):
    """Concrete implementation of the Q&A service."""

    def __init__(self, provider: BaseLLMProvider) -> None:
        super().__init__(provider)

    def validate_input(self, request: QARequest) -> QAInput:
        """
        Validate and normalise the Q&A request.

        TODO:
            - Strip whitespace from both context and question
            - Raise ValueError if either is empty after stripping
            - Return a populated QAInput dataclass

        Args:
            request: Incoming QARequest.

        Returns:
            QAInput dataclass.

        Raises:
            ValueError: If context or question is empty after stripping.
        """
        raise NotImplementedError

    def build_prompt(self, validated_input: QAInput) -> str:
        """
        Construct the Q&A prompt.

        TODO:
            - Ground the model strictly in the provided context
            - Explicitly instruct it NOT to use outside knowledge
            - If the answer is not in the context, set is_answerable to false
              and answer to a clear "I cannot find the answer in the provided context"
            - Instruct LLM to respond ONLY with valid JSON, no markdown fences
            - JSON must contain: answer, confidence (0.0-1.0), is_answerable (bool)

        Args:
            validated_input: Output of validate_input().

        Returns:
            Fully constructed prompt string.
        """
        raise NotImplementedError

    def parse_response(self, raw_response: str) -> QAResponse:
        """
        Parse the raw LLM JSON response into a QAResponse.

        TODO:
            - Strip any accidental markdown fences if present
            - Parse the string as JSON
            - Construct and return a QAResponse
            - Raise ValueError if parsing fails or required fields are missing

        Args:
            raw_response: Raw string returned by the LLM.

        Returns:
            Populated QAResponse.

        Raises:
            ValueError: If the response cannot be parsed.
        """
        raise NotImplementedError
