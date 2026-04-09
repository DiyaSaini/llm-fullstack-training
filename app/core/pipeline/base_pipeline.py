"""
Base pipeline.

Defines the shared execution contract for all feature pipelines.
The pipeline orchestrates the service methods in the correct order.
It knows NOTHING about concrete implementations — only interfaces.
"""

from abc import ABC, abstractmethod
from typing import Any

from app.logging import get_logger

logger = get_logger(__name__)


class BasePipeline(ABC):
    """
    Abstract base pipeline.

    Subclasses inject a service that satisfies BaseService and
    implement `execute()` to orchestrate the call sequence.

    The pipeline is the only caller of service methods.
    Controllers call the pipeline. Services never call the pipeline.
    """

    @abstractmethod
    def execute(self, request: Any) -> Any:
        """
        Run the full processing pipeline for a request.

        Standard sequence:
            1. validated  = service.validate_input(request)
            2. prompt     = service.build_prompt(validated)
            3. raw        = service.provider.generate(prompt)
            4. result     = service.parse_response(raw)
            5. return result

        Args:
            request: Pydantic request schema instance.

        Returns:
            Pydantic response schema instance.

        Raises:
            ValueError: Propagated from validate_input or parse_response.
            LLMProviderError: Propagated from the provider.generate call.
        """
        raise NotImplementedError
