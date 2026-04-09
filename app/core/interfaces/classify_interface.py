"""Classify service interface."""

from abc import abstractmethod

from app.api.v1.schemas.requests.classify import ClassifyRequest
from app.api.v1.schemas.responses.classify import ClassifyResponse
from app.core.interfaces.base_service import BaseService
from app.services.classify.models import ClassifyInput


class ClassifyServiceInterface(BaseService):
    """
    Contract for the text classification service.

    Pipeline call order:
        1. validate_input(request)  → ClassifyInput
        2. build_prompt(input)      → str
        3. call_llm(prompt)         → str
        4. parse_response(raw)      → ClassifyResponse
    """

    @abstractmethod
    def validate_input(self, request: ClassifyRequest) -> ClassifyInput:
        """
        Validate the classify request.

        Args:
            request: Pydantic request with `text` and optional `categories` list.

        Returns:
            ClassifyInput dataclass.

        Raises:
            ValueError: If text is empty.
        """
        raise NotImplementedError

    @abstractmethod
    def build_prompt(self, validated_input: ClassifyInput) -> str:
        """
        Build the classification prompt.

        If `categories` are provided, classify into one of those.
        If not, determine the most appropriate category freely.

        The prompt must instruct the LLM to return JSON:
            {
                "category": "...",
                "confidence": 0.0-1.0,
                "reasoning": "..."
            }

        Args:
            validated_input: Output of validate_input().

        Returns:
            Prompt string.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_response(self, raw_response: str) -> ClassifyResponse:
        """
        Parse JSON response into ClassifyResponse.

        Raises:
            ValueError: If JSON is malformed or fields are missing.
        """
        raise NotImplementedError
