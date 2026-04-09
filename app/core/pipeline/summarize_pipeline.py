"""Summarize pipeline — orchestrates the summarization flow."""

from app.api.v1.schemas.requests.summarize import SummarizeRequest
from app.api.v1.schemas.responses.summarize import SummarizeResponse
from app.core.interfaces.summarize_interface import SummarizeServiceInterface
from app.core.pipeline.base_pipeline import BasePipeline
from app.logging import get_logger

logger = get_logger(__name__)


class SummarizePipeline(BasePipeline):
    """
    Orchestrates the full summarization flow.

    Depends only on SummarizeServiceInterface — never on the
    concrete SummarizeService. This means the pipeline can be
    tested independently by injecting a mock service.
    """

    def __init__(self, service: SummarizeServiceInterface) -> None:
        self.service = service

    def execute(self, request: SummarizeRequest) -> SummarizeResponse:
        """
        Run the summarization pipeline.

        Steps:
            1. Validate and normalise the incoming request
            2. Build the LLM prompt from validated input
            3. Call the LLM provider and get the raw response
            4. Parse the raw response into a structured SummarizeResponse

        Args:
            request: Validated SummarizeRequest from the controller.

        Returns:
            SummarizeResponse with short_summary, detailed_summary, key_points.
        """
        logger.info("SummarizePipeline: starting execution")

        validated = self.service.validate_input(request)
        logger.debug("SummarizePipeline: input validated")

        prompt = self.service.build_prompt(validated)
        logger.debug("SummarizePipeline: prompt built")

        raw = self.service.provider.generate(prompt)
        logger.debug("SummarizePipeline: LLM response received")

        result = self.service.parse_response(raw)
        logger.info("SummarizePipeline: execution complete")

        return result
