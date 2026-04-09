"""Paraphrase pipeline — orchestrates the paraphrase flow."""

from app.api.v1.schemas.requests.paraphrase import ParaphraseRequest
from app.api.v1.schemas.responses.paraphrase import ParaphraseResponse
from app.core.interfaces.paraphrase_interface import ParaphraseServiceInterface
from app.core.pipeline.base_pipeline import BasePipeline
from app.logging import get_logger

logger = get_logger(__name__)


class ParaphrasePipeline(BasePipeline):
    """
    Orchestrates the full paraphrase flow.

    Depends only on ParaphraseServiceInterface.
    """

    def __init__(self, service: ParaphraseServiceInterface) -> None:
        self.service = service

    def execute(self, request: ParaphraseRequest) -> ParaphraseResponse:
        """
        Run the paraphrase pipeline.

        Steps:
            1. Validate and normalise the incoming request
            2. Build the LLM prompt from validated input
            3. Call the LLM provider and get the raw response
            4. Parse the raw response into a structured ParaphraseResponse

        Args:
            request: Validated ParaphraseRequest from the controller.

        Returns:
            ParaphraseResponse with one paraphrased version per requested tone.
        """
        logger.info("ParaphrasePipeline: starting execution")

        validated = self.service.validate_input(request)
        prompt = self.service.build_prompt(validated)
        raw = self.service.provider.generate(prompt)
        result = self.service.parse_response(raw)

        logger.info("ParaphrasePipeline: execution complete")
        return result
