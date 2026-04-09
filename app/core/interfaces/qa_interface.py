"""Question & Answer service interface."""

from abc import abstractmethod

from app.api.v1.schemas.requests.qa import QARequest
from app.api.v1.schemas.responses.qa import QAResponse
from app.core.interfaces.base_service import BaseService
from app.services.qa.models import QAInput


class QAServiceInterface(BaseService):
    """
    Contract for the Q&A service.

    The service answers a question grounded in the provided context text.
    It must NOT answer from general knowledge if the answer is not
    present in the context.

    Pipeline call order:
        1. validate_input(request)  → QAInput
        2. build_prompt(input)      → str
        3. call_llm(prompt)         → str
        4. parse_response(raw)      → QAResponse
    """

    @abstractmethod
    def validate_input(self, request: QARequest) -> QAInput:
        """
        Validate the Q&A request.

        Args:
            request: Pydantic request with `context` and `question`.

        Returns:
            QAInput dataclass.

        Raises:
            ValueError: If context or question is empty.
        """
        raise NotImplementedError

    @abstractmethod
    def build_prompt(self, validated_input: QAInput) -> str:
        """
        Build the Q&A prompt.

        The prompt must:
            - Ground the model strictly in the provided context
            - Instruct it to say "I don't know" if the answer is absent
            - Return JSON:
                {
                    "answer": "...",
                    "confidence": 0.0-1.0,
                    "is_answerable": true | false
                }

        Args:
            validated_input: Output of validate_input().

        Returns:
            Prompt string.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_response(self, raw_response: str) -> QAResponse:
        """
        Parse JSON response into QAResponse.

        Raises:
            ValueError: If JSON is malformed or answer field is missing.
        """
        raise NotImplementedError
