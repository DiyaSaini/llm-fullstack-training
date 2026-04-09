"""
Summarize service interface.

Defines the contract that SummarizeService must fulfil.
The SummarizePipeline depends only on this interface.
"""

from abc import abstractmethod

from app.api.v1.schemas.requests.summarize import SummarizeRequest
from app.api.v1.schemas.responses.summarize import SummarizeResponse
from app.core.interfaces.base_service import BaseService
from app.services.summarize.models import SummarizeInput


class SummarizeServiceInterface(BaseService):
    """
    Contract for the summarization feature service.

    The pipeline will call these methods in this order:
        1. validate_input(request)   → SummarizeInput
        2. build_prompt(input)       → str
        3. call_llm(prompt)          → str          [inherited, do not override]
        4. parse_response(raw)       → SummarizeResponse
    """

    @abstractmethod
    def validate_input(self, request: SummarizeRequest) -> SummarizeInput:
        """
        Validate the summarize request.

        Args:
            request: Incoming Pydantic request with `text` and optional `max_length`.

        Returns:
            SummarizeInput dataclass ready for prompt construction.

        Raises:
            ValueError: If `text` is empty or exceeds maximum allowed length.
        """
        raise NotImplementedError

    @abstractmethod
    def build_prompt(self, validated_input: SummarizeInput) -> str:
        """
        Build the summarization prompt.

        The prompt must instruct the LLM to return a JSON object with:
            {
                "short_summary": "...",   # max 2 sentences
                "detailed_summary": "...", # full paragraph
                "key_points": ["...", ...]  # 3-5 bullet points
            }

        Args:
            validated_input: Output of validate_input().

        Returns:
            Fully constructed prompt string.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_response(self, raw_response: str) -> SummarizeResponse:
        """
        Parse the LLM JSON response into a SummarizeResponse.

        Args:
            raw_response: Raw string from the LLM (expected to be JSON).

        Returns:
            Populated SummarizeResponse instance.

        Raises:
            ValueError: If the response is not valid JSON or missing fields.
        """
        raise NotImplementedError
