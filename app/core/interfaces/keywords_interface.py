"""Keywords extraction service interface."""

from abc import abstractmethod

from app.api.v1.schemas.requests.keywords import KeywordsRequest
from app.api.v1.schemas.responses.keywords import KeywordsResponse
from app.core.interfaces.base_service import BaseService
from app.services.keywords.models import KeywordsInput


class KeywordsServiceInterface(BaseService):
    """
    Contract for the keyword extraction service.

    Pipeline call order:
        1. validate_input(request)  → KeywordsInput
        2. build_prompt(input)      → str
        3. call_llm(prompt)         → str
        4. parse_response(raw)      → KeywordsResponse
    """

    @abstractmethod
    def validate_input(self, request: KeywordsRequest) -> KeywordsInput:
        """
        Validate the keywords request.

        Args:
            request: Pydantic request with `text` and optional `max_keywords` (default 10).

        Returns:
            KeywordsInput dataclass.

        Raises:
            ValueError: If text is empty or max_keywords is out of range (1-20).
        """
        raise NotImplementedError

    @abstractmethod
    def build_prompt(self, validated_input: KeywordsInput) -> str:
        """
        Build the keyword extraction prompt.

        The prompt must instruct the LLM to return JSON:
            {
                "keywords": [
                    {"word": "...", "relevance_score": 0.0-1.0},
                    ...
                ]
            }

        Keywords should be ordered by relevance score descending.

        Args:
            validated_input: Output of validate_input().

        Returns:
            Prompt string.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_response(self, raw_response: str) -> KeywordsResponse:
        """
        Parse JSON response into KeywordsResponse.

        Raises:
            ValueError: If JSON is malformed or keywords list is missing.
        """
        raise NotImplementedError
