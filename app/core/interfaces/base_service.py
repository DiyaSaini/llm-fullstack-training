"""
Base service interface.

Every feature service must extend this class.
It enforces a consistent contract across all services:
    - Receives the LLM provider at construction time
    - Exposes validate_input, build_prompt, parse_response
"""

from abc import ABC, abstractmethod
from typing import Any

from app.providers.llm_provider import BaseLLMProvider


class BaseService(ABC):
    """
    Abstract base for all feature services.

    Subclasses receive a `BaseLLMProvider` at __init__ and must
    implement the three core methods below. The pipeline calls
    these methods in order — services never call the pipeline.

    Attributes:
        provider: The injected LLM provider instance.
    """

    def __init__(self, provider: BaseLLMProvider) -> None:
        self.provider = provider

    @abstractmethod
    def validate_input(self, request: Any) -> Any:
        """
        Validate and pre-process the incoming request object.

        Args:
            request: The Pydantic request schema instance.

        Returns:
            The validated data, ready for prompt construction.
            May return the same object or a transformed dataclass.

        Raises:
            ValueError: If required fields are missing or invalid.
        """
        raise NotImplementedError

    @abstractmethod
    def build_prompt(self, validated_input: Any) -> str:
        """
        Construct the prompt string to send to the LLM.

        Args:
            validated_input: Output from validate_input().

        Returns:
            A fully formed prompt string.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_response(self, raw_response: str) -> Any:
        """
        Parse the raw LLM response string into a structured object.

        Args:
            raw_response: Raw text returned by the LLM provider.

        Returns:
            A Pydantic response model or internal dataclass.

        Raises:
            ValueError: If the response cannot be parsed.
        """
        raise NotImplementedError
