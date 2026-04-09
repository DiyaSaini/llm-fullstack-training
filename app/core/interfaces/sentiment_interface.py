"""Sentiment analysis service interface."""

from abc import abstractmethod

from app.api.v1.schemas.requests.sentiment import SentimentRequest
from app.api.v1.schemas.responses.sentiment import SentimentResponse
from app.core.interfaces.base_service import BaseService
from app.services.sentiment.models import SentimentInput


class SentimentServiceInterface(BaseService):
    """
    Contract for the sentiment analysis service.

    Pipeline call order:
        1. validate_input(request)  → SentimentInput
        2. build_prompt(input)      → str
        3. call_llm(prompt)         → str
        4. parse_response(raw)      → SentimentResponse
    """

    @abstractmethod
    def validate_input(self, request: SentimentRequest) -> SentimentInput:
        """
        Validate the sentiment request.

        Args:
            request: Pydantic request with `text`.

        Returns:
            SentimentInput dataclass.

        Raises:
            ValueError: If text is empty.
        """
        raise NotImplementedError

    @abstractmethod
    def build_prompt(self, validated_input: SentimentInput) -> str:
        """
        Build the sentiment analysis prompt.

        The prompt must instruct the LLM to return JSON:
            {
                "sentiment": "positive" | "negative" | "neutral" | "mixed",
                "score": -1.0 to 1.0,
                "reasoning": "...",
                "emotions": ["joy", "anger", ...]   # detected emotions
            }

        Args:
            validated_input: Output of validate_input().

        Returns:
            Prompt string.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_response(self, raw_response: str) -> SentimentResponse:
        """
        Parse JSON response into SentimentResponse.

        Raises:
            ValueError: If JSON is malformed or sentiment field is missing.
        """
        raise NotImplementedError
