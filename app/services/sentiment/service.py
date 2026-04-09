"""
Sentiment service — concrete implementation.

ASSOCIATE 4 — this is your primary file to implement.

Steps to get started:
    1. Read app/core/interfaces/sentiment_interface.py carefully
    2. Read app/core/pipeline/sentiment_pipeline.py to understand call order
    3. Read app/services/sentiment/models.py for the SentimentInput dataclass
    4. Read app/api/v1/schemas/requests/sentiment.py for incoming request shape
    5. Read app/api/v1/schemas/responses/sentiment.py for expected response shape
    6. Implement each method below
    7. Run your tests: pytest tests/test_sentiment.py -v
    8. Run your script: python scripts/run_sentiment.py --text "Your text here"
"""

from app.api.v1.schemas.requests.sentiment import SentimentRequest
from app.api.v1.schemas.responses.sentiment import SentimentResponse
from app.core.interfaces.sentiment_interface import SentimentServiceInterface
from app.logging import get_logger
from app.providers.llm_provider import BaseLLMProvider
from app.services.sentiment.models import SentimentInput

logger = get_logger(__name__)


class SentimentService(SentimentServiceInterface):
    """Concrete implementation of the sentiment analysis service."""

    def __init__(self, provider: BaseLLMProvider) -> None:
        super().__init__(provider)

    def validate_input(self, request: SentimentRequest) -> SentimentInput:
        """
        Validate and normalise the sentiment request.

        TODO:
            - Strip whitespace from text
            - Raise ValueError if text is empty after stripping
            - Return a populated SentimentInput dataclass

        Args:
            request: Incoming SentimentRequest.

        Returns:
            SentimentInput dataclass.

        Raises:
            ValueError: If text is empty after stripping.
        """
        raise NotImplementedError

    def build_prompt(self, validated_input: SentimentInput) -> str:
        """
        Construct the sentiment analysis prompt.

        TODO:
            - Instruct the LLM to classify sentiment as one of:
              positive, negative, neutral, mixed
            - Ask for a score between -1.0 (very negative) and 1.0 (very positive)
            - Ask for a reasoning explanation
            - Ask for a list of detected emotions
            - Instruct LLM to respond ONLY with valid JSON, no markdown fences
            - JSON must contain: sentiment, score, reasoning, emotions

        Args:
            validated_input: Output of validate_input().

        Returns:
            Fully constructed prompt string.
        """
        raise NotImplementedError

    def parse_response(self, raw_response: str) -> SentimentResponse:
        """
        Parse the raw LLM JSON response into a SentimentResponse.

        TODO:
            - Strip any accidental markdown fences if present
            - Parse the string as JSON
            - Validate that sentiment is one of the allowed values
            - Construct and return a SentimentResponse
            - Raise ValueError if parsing fails or required fields are missing

        Args:
            raw_response: Raw string returned by the LLM.

        Returns:
            Populated SentimentResponse.

        Raises:
            ValueError: If the response cannot be parsed or sentiment is invalid.
        """
        raise NotImplementedError
