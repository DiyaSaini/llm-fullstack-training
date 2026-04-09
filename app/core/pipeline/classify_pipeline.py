"""Classify pipeline — orchestrates the text classification flow."""

from app.api.v1.schemas.requests.classify import ClassifyRequest
from app.api.v1.schemas.responses.classify import ClassifyResponse
from app.core.interfaces.classify_interface import ClassifyServiceInterface
from app.core.pipeline.base_pipeline import BasePipeline
from app.logging import get_logger

logger = get_logger(__name__)


class ClassifyPipeline(BasePipeline):
    """
    Orchestrates the full text classification flow.

    Depends only on ClassifyServiceInterface.
    """

    def __init__(self, service: ClassifyServiceInterface) -> None:
        self.service = service

    def execute(self, request: ClassifyRequest) -> ClassifyResponse:
        """
        Run the classification pipeline.

        Steps:
            1. Validate and normalise the incoming request
            2. Build the LLM prompt from validated input
            3. Call the LLM provider and get the raw response
            4. Parse the raw response into a structured ClassifyResponse

        Args:
            request: Validated ClassifyRequest from the controller.

        Returns:
            ClassifyResponse with category, confidence, and reasoning.
        """
        logger.info("ClassifyPipeline: starting execution")

        validated = self.service.validate_input(request)
        prompt = self.service.build_prompt(validated)
        raw = self.service.provider.generate(prompt)
        result = self.service.parse_response(raw)

        logger.info("ClassifyPipeline: execution complete")
        return result
